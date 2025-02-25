"""Module algorithm.py"""
import typing

import arviz
import pandas as pd
import pymc
import pymc.sampling.jax

import config


class Algorithm:
    """
    The multi-level algorithm
    """

    def __init__(self, arguments: dict) -> None:
        """
        Constructor
        """

        self.__priors = arguments['priors']

        self.__configurations = config.Config()

    def exc(self, data: pd.DataFrame) -> typing.Tuple[pymc.model.core.Model, arviz.data.InferenceData]:
        """

        :param data: <br>The training data of a board; a board consists of one or more hospitals/institutions.<br>
        :return:
        """

        timings = list(range(data.shape[0]))

        coords = {'obs_id': timings}

        with pymc.Model(coords=coords) as model:

            # The data containers
            points = pymc.Data('points', timings, dims='obs_id')
            observations = pymc.Data('observations', data['dt'].to_numpy(), dims='obs_id')

            # Setting priors for each coefficient in the AR process
            coefficients = pymc.Normal(
                'coefficients', mu=self.__priors['coefficients']['mu'],
                sigma=self.__priors['coefficients']['sigma'], size=self.__priors['coefficients']['size'])
            sigma = pymc.HalfNormal('sigma', self.__priors['sigma'])
            degree = pymc.Uniform('degree', lower=self.__priors['degree']['lower'], upper=self.__priors['degree']['upper'])

            # Initialisation per ...
            init = pymc.Normal.dist(
                self.__priors['init']['mu'], self.__priors['init']['sigma'], size=self.__priors['init']['size']
            )

            # Autoregressive process with p lags; lags = self.__priors['coefficients']['size'] - 1
            process = pymc.AR(
                'ar', coefficients, sigma=sigma, init_dist=init, constant=True,
                steps=points.eval().shape[0] - (self.__priors['coefficients']['size'] - 1),
                dims='obs_id')

            # Likelihood
            pymc.StudentT('likelihood', mu=process, sigma=sigma, nu=degree, observed=observations, dims='obs_id')

            # Sampling
            details = pymc.sample_prior_predictive()

            details.extend(pymc.sample(3000, random_seed=100, target_accept=0.95))
            details.extend(pymc.sample_posterior_predictive(details))

        return model, details
