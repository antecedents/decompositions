"""Module futures.py"""

import numpy as np

import config

class Futures:
    """
    For estimating future values
    """

    def __init__(self, points: np.ndarray):
        """

        :param points:
        """

        self.__points = points

        # Configurations
        self.__configurations = config.Config()
        self.__rng = np.random.default_rng(self.__configurations.seed)

    def _forecast(self, intercept, lc, noise, forecast):
        """

        :param intercept: constant coefficient
        :param lc: lag coefficients
        :param noise:
        :param forecast: # of forecast points
        :return:
        """

        n_points = len(self.__points)

        # The underlying structure of the draws is → the shape of the training data variable + # of forecasts
        draws = np.zeros((self.__points.shape[0] + forecast, self.__points.shape[1]))

        # Fill the new array with the observed data
        draws[:n_points] = self.__points[:]

        # Drawing
        for i in range(forecast):
            ar_ = np.sum(lc[:, 0] * draws[(n_points + i - self.__configurations.n_lags):(n_points + i)])
            mean = intercept + ar_
            draws[n_points + i] = self.__rng.normal(mean, noise)

        # Replace all observed data with NaN
        draws[:-forecast - 1] = np.nan

        return draws

    def exc(self):
        pass
