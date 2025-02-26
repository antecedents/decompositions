import pymc

class Forecasting:

    def __init__(self, arguments: dict):

        self.__arguments = arguments

    def exc(self, model: pymc.model.core.Model, n_instances: int):

        starting = n_instances - self.__arguments['n_lags']
        ending = n_instances + self.__arguments['ahead']

        with model:
            model.add_coords({'id_estimating': range(starting, ending, 1)})
            model.add_coords({'id_forecasting': range(n_instances, ending, 1)})
