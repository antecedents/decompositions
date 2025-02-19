"""Module boundaries.py"""
import numpy as np

import config


class Boundaries:
    """
    Boundaries
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

    def exc(self, d_ppc: np.ndarray):
        """

        :param d_ppc: Posterior draws
        :return:
        """

        lower = np.percentile(
            d_ppc[-self.__configurations.ahead:,:,0], min(self.__configurations.interval), axis=1)
        upper = np.percentile(
            d_ppc[-self.__configurations.ahead:,:,0], max(self.__configurations.interval), axis=1)

        return lower, upper
