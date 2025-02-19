"""Module futures.py"""
import numpy as np
import pandas as pd

import config


class Futures:
    """
    For estimating future values
    """

    def __init__(self, points: pd.DataFrame):
        """

        :param points:
        """

        self.__points = points

        # Configurations
        self.__configurations = config.Config()

        # Random Number Generator
        self.__rng = np.random.default_rng(self.__configurations.seed)

    def __forecast(self, intercept: np.ndarray, lc: np.ndarray, noise: np.ndarray, forecast: int):
        """

        :param intercept: Intercept, constant coefficient, draws
        :param lc: Lag coefficients draws
        :param noise: Noise draws
        :param forecast: # of forecast points
        :return:
        """

        n_points = self.__points.shape[0]

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

    def exc(self, d_intercept: np.ndarray, d_lc: np.ndarray, d_noise: np.ndarray) -> np.ndarray:
        """

        :param d_intercept: Intercept draws
        :param d_lc: Lag coefficient draws
        :param d_noise: Noise draws
        :return:
        """

        # Vectorized forecast function to handle multiple parameter draws
        forecast = np.vectorize(
            self.__forecast,
            signature='(v),(l,v,v),(v)->(o,v)',
            excluded=('self', 'forecast'),
        )

        # Forecasting weeks ahead
        d_ppc = forecast(intercept=d_intercept, lc=d_lc, noise=d_noise, forecast=self.__configurations.ahead)
        d_ppc = np.swapaxes(d_ppc, 0, 1)

        return d_ppc
