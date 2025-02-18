"""Module algorithm.py"""
import typing
import numpy as np
import pandas as pd
import pymc
import pymc.sampling.jax

import arviz.data

import config
import src.modelling.marginals


class Algorithm:
    """
    The multi-level algorithm
    """

    def __init__(self) -> None:
        """
        Constructor
        """

        self.__configurations = config.Config()
        self.__marginals = src.modelling.marginals.Marginals()

    def exc(self, n_lags: int, n_eqs: int, data: pd.DataFrame, group_field: str, prior_checks: bool = False) -> (
            typing.Tuple)[pymc.model.core.Model, arviz.data.InferenceData]:
        """

        :param n_lags: <br># of non-constant coefficients<br>
        :param n_eqs: <br># of independent variables.  Beware, this algorithm is inappropriate for cases whereby
                      there are two or more variates because it does not consider multi-variate covariance.<br>
        :param data: <br>The training data.<br>
        :param group_field: <br>The field that identifies an instance's group<br>
        :param prior_checks: <br>Focusing on priors only?<br>
        :return:
        """

        cols = [col for col in data.columns if col != group_field]
        coords = {'lags': np.arange(n_lags) + 1,
                  'equations': cols}

        groups = data[group_field].unique()

        with pymc.Model(coords=coords) as model:

            # Hierarchical Priors
            alpha_hat_location = pymc.Normal('alpha_hat_location', mu=0, sigma=0.1)
            alpha_hat_scale = pymc.InverseGamma('alpha_hat_scale', alpha=3, beta=0.5)
            beta_hat_location = pymc.Normal('beta_hat_location', mu=0, sigma=0.1)
            beta_hat_scale = pymc.InverseGamma('beta_hat_scale', alpha=3, beta=0.5)

            # By institution
            for grp in groups:

                excerpt = data[data[group_field] == grp][cols]
                z_scale_beta = pymc.InverseGamma(f'z_scale_beta_{grp}', alpha=3, beta=0.5)
                z_scale_alpha = pymc.InverseGamma(f'z_scale_alpha_{grp}', alpha=3, beta=0.5)
                lc = pymc.Normal(
                    f'lc_{grp}',
                    mu=beta_hat_location,
                    sigma=beta_hat_scale * z_scale_beta,
                    dims=['equations', 'lags'],
                )
                alpha = pymc.Normal(
                    f'alpha_{grp}',
                    mu=alpha_hat_location,
                    sigma=alpha_hat_scale * z_scale_alpha,
                    dims=('equations',)
                )

                beta_x = self.__marginals.exc(lc=lc, n_equations=n_eqs, n_lags=n_lags, segment=excerpt)
                beta_x = pymc.Deterministic(f'beta_x_{grp}', beta_x)
                mean = alpha + beta_x

                # Likelihood
                sigma = pymc.HalfNormal(f'sigma_{grp}',
                                        sigma=self.__configurations.priors['noise']['sigma'], dims=['equations'])
                pymc.Normal(f'likelihood_{grp}', mu=mean, sigma=sigma, observed=excerpt.values[n_lags:])

            if prior_checks:
                idata = pymc.sample_prior_predictive(random_seed=self.__configurations.seed)
                return model, idata
            else:
                idata = pymc.sample_prior_predictive(random_seed=self.__configurations.seed)
                idata.extend(pymc.sampling.jax.sample_blackjax_nuts(
                    draws=2000, random_seed=self.__configurations.seed, chains=4, target_accept=0.95))
                idata.extend(pymc.sample_posterior_predictive(idata))

        return model, idata
