import logging
import pandas as pd

class Algorithm:

    def __init__(self, data: pd.DataFrame):
        """

        :param data:
        """

        self.__data = data

    def exc(self, group: str):
        """

        :param group:
        :return:
        """

        columns = [column for column in self.__data.columns if column != group]
        logging.info(columns)

