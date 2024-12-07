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

        temporary: pd.DataFrame = src.modelling.temporary.Temporary().exc()
        temporary.sort_values(by=['health_board_code', 'hospital_code', 'week_ending_date'], ascending=True, inplace=True)
        logging.info(temporary)

        src.modelling.algorithm.Algorithm(data=temporary[self.__fields]).exc(group='hospital_code')
