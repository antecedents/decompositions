"""Module forecasting.py"""
import arviz
import pymc


class Forecasting:
    """
    Forecasting
    """

    def __init__(self, arguments: dict):
        """

        :param arguments:
        """

        self.__arguments = arguments

    def exc(self, model: pymc.model.core.Model, details: arviz.data.InferenceData):
        """

        :param model:
        :param details:
        :return:
        """

        n_instances = details.get('observed_data').get('id_instances').shape[0]

        # Start by centring vis-à-vis the last lag cycle
        starting = n_instances - self.__arguments['n_lags']
        ending = n_instances + self.__arguments['ahead']

        # Predicting
        with model:

            model.add_coords({'id_estimating': range(starting, ending, 1)})
            model.add_coords({'id_forecasting': range(n_instances, ending, 1)})

            # Auto-regression
            arc = pymc.AR(
                'arc',
                init_dist=pymc.DiracDelta.dist(model['ar'][..., -1]),
                rho=model['coefficients'],
                sigma=model['sigma'],
                constant=True, dims='id_estimating')

            # The futures likelihood
            pymc.StudentT(
                'future', mu=arc[self.__arguments.get('n_lags'):],
                sigma=model['sigma'], nu=model['degree'], dims='id_forecasting')

            # Predict outcomes and probabilities via the updated values
            predictions = pymc.sample_posterior_predictive(
                details, var_names=['likelihood', 'future'], predictions=True, random_seed=self.__arguments['seed'])

        return predictions
