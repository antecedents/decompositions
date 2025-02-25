"""Module interface.py"""

import boto3
import pandas as pd


class Interface:
    """
    Interface
    """

    def __init__(self, training: pd.DataFrame, testing: pd.DataFrame, connector: boto3.session.Session):
        """

        :param training:
        :param testing:
        :param connector:
        """

        self.__training = training
        self.__testing = testing
        self.__connector = connector

    def __get_data(self, code: str) -> pd.DataFrame:
        """

        :param code:
        :return:
        """

        frame: pd.DataFrame = self.__training.loc[self.__training['hospital_code'] == code, :]
        frame.sort_values(by=['week_ending_date'], ascending=True, inplace=True)

        return frame

    def exc(self):
        pass
