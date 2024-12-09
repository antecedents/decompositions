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

        # Temporarily, read-in the local copy of the Amazon data set.
        self.__temporary: pd.DataFrame = src.modelling.temporary.Temporary().exc()

        # How many hospitals per board?
        self.__frequencies = self.__temporary.copy()[['health_board_code', 'hospital_code']].drop_duplicates().value_counts(
            subset='health_board_code', ascending=False)

    def __strategy(self, health_board_code: str):
        """
        Either:<br>
        A Bayesian hierarchical model
             <ul><li>Per health board</li>
             <li>Covering all boards</li></ul>

        :param health_board_code:
        :return:
        """

        return self.__temporary.copy().loc[
            self.__temporary['health_board_code'] == health_board_code, self.__fields]

    def exc(self):
        """

        :return:
        """

        # Initially, focus on the health board that has the largest number of hospitals.
        logging.info(self.__frequencies.index.name)
        logging.info(self.__frequencies.index[0])
        data = self.__strategy(health_board_code=self.__frequencies.index[0])

        # Hence
        src.modelling.algorithm.Algorithm(data=data).exc(
            n_lags=2, n_equations=3, group='hospital_code', prior_predictive_check=False)
