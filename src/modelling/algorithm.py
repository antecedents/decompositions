import logging
import pandas as pd
import numpy as np

class Algorithm:

    def __init__(self, data: pd.DataFrame):
        """

        :param data:
        """

        self.__data = data

    def exc(self, n_lags: int, n_equations: int, group: str):
        """

        :param n_lags:
        :param n_equations:
        :param group:
        :return:
        """

        columns = [column for column in self.__data.columns if column != group]
        logging.info(columns)

        coordinates = {'lags': np.arange(n_lags),
                       'equations': columns,
                       'cv': columns}
        logging.info(coordinates)

        groups = self.__data[group].unique()
        logging.info(groups)
