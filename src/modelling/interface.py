"""Module interface.py"""
import logging
import pandas as pd

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

    def exc(self):
        """

        :return:
        """

        boards = self.__training['health_board_code'].unique()

        for board in boards:

            logging.info(board)

            # model, idata = src.modelling.algorithm.Algorithm().exc(n_lags=, n_eqs=, df=, group_field=, prior_checks=False)
            # model.named_vars
