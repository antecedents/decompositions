"""Module algorithm.py"""
import os
import typing

import arviz
import numpy as np
import numpyro
import pandas as pd
import pymc
import pymc.sampling.jax
import pytensor


class Algorithm:
    """
    Vis-à-vis trend component modelling.
    """

    os.environ['XLA_FLAGS'] = '--xla_disable_hlo_passes=constant_folding'

    pytensor.config.blas__ldflags = '-llapack -lblas -lcblas'

    def __init__(self, training: pd.DataFrame, dates: np.ndarray, arguments: dict) -> None:
        """

        :param training: An institution's training data
        :param arguments: A set of modelling & supplementary arguments
        """

        # Data
        self.__training = training
        self.__sequence = self.__training['trend'].to_numpy()
        self.__indices = np.expand_dims(np.arange(self.__training.shape[0]), axis=1)

        self.__dates = dates
        self.__arguments = arguments

    # noinspection PyTypeChecker
    # pylint: disable-next=R0915,R0914
    def exc(self) -> typing.Tuple[pymc.model.Model, arviz.InferenceData, pd.DataFrame]:
        """
        Notes<br>
        ------<br>

        Due to the number of variables that the Bayesian algorithm/model requires, rule R0914 does
        not apply to this method; R0194 -> Too many local variables (16/15) (too-many-locals).  The
        pylint decoration disables the rule.  Similarly, statements: R0915.<br><br>

        For more about this method's covariance function options visit https://docs.pymc.io/api/gp/cov.html

        :return:
        """

        trend: dict = self.__arguments.get('tc')

        numpyro.set_host_device_count(trend.get('chains'))

        # Indices for forecasting beyond training data
        abscissae = np.arange(self.__training.shape[0] + (2 * self.__arguments.get('ahead')))[:, None]

        with pymc.Model() as model_:

            # The data containers
            points = pymc.Data('points', self.__indices)
            observations = pymc.Data('observations', self.__sequence)

            # Covariance function: Initialise the spatial scaling (ℓ) and variance control (η) parameters
            spatial_scaling = pymc.Gamma(
                'spatial_scaling',
                alpha=trend.get('covariance').get('spatial_scaling').get('alpha'),
                beta=trend.get('covariance').get('spatial_scaling').get('beta'))

            variance_control = pymc.HalfCauchy(
                'variance_control',
                beta=trend.get('covariance').get('variance_control').get('beta'))

            cov = variance_control**2 * pymc.gp.cov.ExpQuad(input_dim=1, ls=spatial_scaling)

            # Specify the Gaussian Process (GP); the default mean function is `Zero`.
            gp_ = pymc.gp.Marginal(cov_func=cov)

            # Marginal Likelihood
            ml_sigma = pymc.HalfCauchy('ml_sigma', beta=trend.get('ml_sigma').get('beta'))
            gp_.marginal_likelihood('ml', X=points, y=observations, sigma=ml_sigma)

            # Inference
            details_ = pymc.sample(
                draws=trend.get('draws'),
                tune=trend.get('tune'),
                chains=trend.get('chains'),
                target_accept=trend.get('target_accept'),
                random_seed=self.__arguments.get('seed'),
                nuts_sampler=trend.get('nuts_sampler'),
                nuts_sampler_kwargs={
                    'chain_method': trend.get('chain_method'),
                    'postprocessing_backend': self.__arguments.get('device')}
            )

            mu, variance = gp_.predict(
                abscissae, point=arviz.extract(details_.get('posterior'), num_samples=1).squeeze(),
                diag=True, pred_noise=False)
            forecasts_ = pd.DataFrame(
                data={'abscissa': abscissae.squeeze(), 'date': self.__dates, 'mu': mu, 'std': np.sqrt(variance)})

        return model_, details_, forecasts_
