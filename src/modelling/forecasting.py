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

            arc = pymc.AR(
                'arc',
                init_dist=pymc.DiracDelta.dist(model['ar'][..., -1]),
                rho=model['coefficients'],
                sigma=model['sigma'],
                constant=True, dims='id_estimating')

            start: int = self.__arguments['n_lags']
            pymc.StudentT('future', mu=arc[start:], sigma=model['sigma'], nu=model['degree'], dims='id_forecasting')
