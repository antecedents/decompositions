"""Module interface.py"""

import boto3
import pandas as pd


class Interface:
    """
    Interface
    """

    def __init__(self, training: pd.DataFrame, connector: boto3.session.Session, stamp: str):
        """

        :param training:
        :param connector:
        :param stamp:
        """

        self.__training = training
        self.__connector = connector
        self.__stamp = stamp

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
