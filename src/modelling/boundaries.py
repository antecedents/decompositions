"""Module boundaries.py"""
import numpy as np

import config


class Boundaries:
    """
    Boundaries
    """

    def __init__(self, arguments: dict):
        """
        Constructor
        """

        self.__arguments = arguments

        self.__configurations = config.Config()

    def exc(self, d_ppc: np.ndarray):
        """

        :param d_ppc: Posterior draws
        :return:
        """

        lower = np.percentile(
            d_ppc[-self.__arguments['ahead']:,:,0], min(self.__arguments['interval']), axis=1)
        upper = np.percentile(
            d_ppc[-self.__arguments['ahead']:,:,0], max(self.__arguments['interval']), axis=1)

        return lower, upper
