"""Module estimates.py"""
import pymc

import config

class Estimates:
    """
    For estimating future values
    """

    def __init__(self, n_timings: int, ahead: int):
        """

        :param n_timings:
        :param ahead:
        """

        self.__n_timings = n_timings
        self.__prediction_length = self.__n_timings + ahead

        # Configurations
        self.__configurations = config.Config()

    def exc(self, ARMODEL: pymc.model.core.Model):

        with ARMODEL:

            ARMODEL.add_coords({'obs_id_ext': range(
                self.__n_timings - self.__configurations.seasons, self.__prediction_length, 1)})
            ARMODEL.add_coords({'obs_id_original': range(self.__n_timings, self.__prediction_length, 1)})
