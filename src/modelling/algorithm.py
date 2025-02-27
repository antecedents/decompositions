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

        self.__arguments = arguments
        self.__priors: dict = self.__arguments.get('priors')

        # Configurations
        self.__configurations = config.Config()

    def exc(self, data: pd.DataFrame) -> typing.Tuple[pymc.model.core.Model, arviz.data.InferenceData]:
        """

        :param data: <br>The training data of a board; a board consists of one or more hospitals/institutions.<br>
        :return:
        """

        timings = list(range(data.shape[0]))

        coords = {'id_instances': timings}

        with pymc.Model(coords=coords) as model:

            # The data containers
            points = pymc.Data('points', timings, dims='id_instances')
            observations = pymc.Data('observations', data['dt'].to_numpy(), dims='id_instances')

            # Setting priors for each coefficient in the AR process
            coefficients = pymc.Normal(
                'coefficients', mu=self.__priors.get('coefficients').get('mu'),
                sigma=self.__priors.get('coefficients').get('sigma'),
                size=self.__priors.get('coefficients').get('size'))
            sigma = pymc.HalfNormal('sigma', self.__priors.get('sigma'))

            # Initialisation per non-constant coefficient
            init = pymc.Normal.dist(
                self.__priors.get('init').get('mu'), self.__priors.get('init').get('sigma'),
                size=self.__priors.get('init').get('size')
            )

            # Autoregressive process with p lags; lags = self.__priors['coefficients']['size'] - 1
            process = pymc.AR(
                'ar', coefficients, sigma=sigma, init_dist=init, constant=True,
                steps=points.eval().shape[0] - (self.__priors.get('coefficients').get('size') - 1),
                dims='id_instances')

            # Likelihood prior
            degree = pymc.Uniform(
                'degree', lower=self.__priors.get('degree').get('lower'),
                upper=self.__priors.get('degree').get('upper'))

            # Likelihood
            pymc.StudentT('likelihood', mu=process, sigma=sigma, nu=degree, observed=observations, dims='id_instances')

            # Sampling
            details = pymc.sample_prior_predictive(random_seed=self.__arguments.get('seed'))
            details.extend(pymc.sample(3000, random_seed=self.__arguments.get('seed'), target_accept=0.95))
            details.extend(pymc.sample_posterior_predictive(details, random_seed=self.__arguments.get('seed')))

        return model, details
