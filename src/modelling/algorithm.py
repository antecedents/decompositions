import logging
import pandas as pd
import numpy as np
import pymc
import src.modelling.autoregression


class Algorithm:

    def __init__(self, data: pd.DataFrame):
        """

        :param data:
        """

        self.__data = data

        self.__autoregression = src.modelling.autoregression.Autoregression()

    def exc(self, n_lags: int, n_equations: int, group: str):
        """

        :param n_lags:
        :param n_equations:
        :param group:
        :return:
        """

        columns = [column for column in self.__data.columns if column != group]
        logging.info(columns)

        coordinates = {'lags': np.arange(n_lags),
                       'equations': columns,
                       'cv': columns}
        logging.info(coordinates)

        groups = self.__data[group].unique()
        logging.info(groups)

        with pymc.Model(coords=coordinates) as model:

            # Priors
            rho = pymc.Beta('rho', alpha=1.5, beta=1.5)

            location_alpha = pymc.Normal('location_alpha', mu=0, sigma=0.1)
            scale_alpha = pymc.InverseGamma('scale_alpha', mu=2, sigma=0.5)

            location_beta = pymc.Normal('location_beta', mu=0, sigma=0.1)
            scale_beta = pymc.InverseGamma('scale_beta', mu=2, sigma=0.5)

            # Covariance Matrix: cholesky, correlations, deviations
            cholesky, _, _ = pymc.LKJCholeskyCov('', eta=1.25, n=n_equations, sd_dist=pymc.Exponential.dist(lam=2.0))

            # Groups: Institutions
            for group in groups:

                frame = self.__data[self.__data[group] == group][columns]
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
                    f'noise_cholesky_{group}', eta=10, n=n, sd_dist=pymc.Exponential.dist(lam=2.0)
                )
                omega = pymc.Deterministic(f'omega_{group}', rho * cholesky + (1 - rho) * noise_cholesky)
                observations = pymc.MvNormal(f'observations_{group}', mu=mean, chol=omega, observed=frame.values[n_lags:])

