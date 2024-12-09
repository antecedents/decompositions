import logging
import pandas as pd
import numpy as np
import pymc
import pymc.sampling.jax

import config
import src.modelling.autoregression


class Algorithm:

    def __init__(self, data: pd.DataFrame):
        """

        :param data:
        """

        self.__data = data

        self.__configurations = config.Config()
        self.__autoregression = src.modelling.autoregression.Autoregression()

    def exc(self, n_lags: int, n_equations: int, group: str, prior_predictive_check: bool):
        """

        :param n_lags:
        :param n_equations:
        :param group:
        :param prior_predictive_check:
        :return:
        """

        columns = [column for column in self.__data.columns if column != group]
        coordinates = {'lags': np.arange(n_lags),
                       'equations': columns,
                       'cv': columns}
        groups = self.__data[group].unique()

        with pymc.Model(coords=coordinates) as model:

            # Priors
            rho = pymc.Beta('rho', alpha=1.5, beta=1.5)

            location_alpha = pymc.Normal('location_alpha', mu=0, sigma=0.1)
            scale_alpha = pymc.InverseGamma('scale_alpha', mu=2, sigma=0.5)

            location_beta = pymc.Normal('location_beta', mu=0, sigma=0.1)
            scale_beta = pymc.InverseGamma('scale_beta', mu=2, sigma=0.5)

            # Covariance Matrix: cholesky, correlations, deviations
            cholesky, _, _ = pymc.LKJCholeskyCov('cholesky', eta=1.25, n=n_equations, sd_dist=pymc.Exponential.dist(lam=1))

            # Groups: Institutions
            for group in groups:

                logging.info('Next: %s', group)

                frame: pd.DataFrame = self.__data.loc[self.__data['hospital_code'] == group][columns]

                z_scale_beta = pymc.InverseGamma(f'z_scale_beta_{group}', 3, 0.5)
                z_scale_alpha = pymc.InverseGamma(f'z_scale_alpha_{group}', 3, 0.5)

                _product_beta = (scale_beta * z_scale_beta)
                lag_coefficients = pymc.Normal(
                    f'lag_coefficients_{group}',
                    mu=location_beta,
                    sigma=_product_beta,
                    dims=['equations', 'lags', 'cv'],
                )

                _product_alpha = (scale_alpha * z_scale_alpha)
                alpha = pymc.Normal(
                    f'alpha_{group}',
                    mu=location_alpha,
                    sigma=_product_alpha,
                    dims=('equations',),
                )

                beta_values = self.__autoregression.exc(lag_coefficients, n_equations, n_lags, frame)
                beta_values = pymc.Deterministic(f'beta_values_{group}', beta_values)
                mean = alpha + beta_values

                n = frame.shape[1]
                noise_cholesky, _, _ = pymc.LKJCholeskyCov(
                    f'noise_cholesky_{group}', eta=10, n=n, sd_dist=pymc.Exponential.dist(lam=1)
                )
                omega = pymc.Deterministic(f'omega_{group}', rho * cholesky + (1 - rho) * noise_cholesky)
                observations = pymc.MvNormal(f'observations_{group}', mu=mean, chol=omega, observed=frame.values[n_lags:])

            if prior_predictive_check:
                idata = pymc.sample_prior_predictive()
                return model, idata
            else:
                logging.info('Sampling?')
                idata = pymc.sample_prior_predictive()
                logging.info('Extending?')
                idata.extend(pymc.sampling.jax.sample_jax_nuts(
                    draws=2000, random_seed=self.__configurations.seed, nuts_sampler='blackjax'))
                pymc.sample_posterior_predictive(idata, extend_inferencedata=True)

            return model, idata
