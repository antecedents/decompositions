"""Module interface.py"""
import logging
import pandas as pd

import src.modelling.algorithm
import src.modelling.temporary


class Interface:
    """
    Interface
    """

    def __init__(self):

        self.__fields = ['hospital_code', 'n_attendances']

    def exc(self):
        """

        :return:
        """

        # Temporarily, read-in the local copy of the Amazon data set.
        temporary: pd.DataFrame = src.modelling.temporary.Temporary().exc()

        # Initially, focus on the health board that has the largest number of hospitals.
        frequencies = temporary[['health_board_code', 'hospital_code']].drop_duplicates().value_counts(subset='health_board_code', ascending=False)
        logging.info(frequencies)
        logging.info(frequencies.index.name)
        logging.info(frequencies.index[0])

        # src.modelling.algorithm.Algorithm(data=temporary[self.__fields]).exc(n_lags=2, n_equations=3, group='hospital_code')
