"""Module interface.py"""
import logging
import pandas as pd

import config
import src.modelling.algorithm


class Interface:
    """
    Interface
    """

    def __init__(self, training: pd.DataFrame):
        """

        :param training:
        """

        self.__training: pd.DataFrame = training

        # Configurations, etc
        self.__configurations = config.Config()
        self.__algorithms = src.modelling.algorithm.Algorithm()

    def __get_data(self, board: str) -> pd.DataFrame:
        """

        :param board:
        :return:
        """

        frame: pd.DataFrame = self.__training.loc[self.__training['health_board_code'] == board, :]
        frame.sort_values(by=['week_ending_date'], ascending=True, inplace=True)

        return frame

    def __fundamentals(self, frame: pd.DataFrame):
        """

        :return:
        """

        # model, idata = slf.__algorithms.exc(n_lags=, n_eqs=, df=, group_field=, prior_checks=False)
        # model.named_vars

    def exc(self):
        """

        :return:
        """

        boards = self.__training['health_board_code'].unique()

        for board in boards:
            data = self.__get_data(board=board)
