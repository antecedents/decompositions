"""Module boundaries.py"""
import numpy as np

import config


class Boundaries:
    """
    Boundaries
    """

    def __init__(self, computations: list):
        """

        :param computations: Whereby computations[i][0] encodes the posteriors, and computations[i][1] is
                             the hospital/institution code
        """

        self.__configurations = config.Config()

    def exc(self, d_ppc: np.ndarray):
        """

        :param d_ppc:
        :return:
        """

        lower = np.percentile(
            d_ppc[-self.__configurations.ahead:,:,0], min(self.__configurations.interval), axis=1)
        upper = np.percentile(
            d_ppc[-self.__configurations.ahead:,:,0], max(self.__configurations.interval), axis=1)

        return lower, upper
