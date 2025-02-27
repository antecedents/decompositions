"""Module interface.py"""

import boto3
import pandas as pd

import src.modelling.algorithm
import src.modelling.forecasting


class Interface:
    """
    Interface
    """

    def __init__(self, training: pd.DataFrame, testing: pd.DataFrame, arguments: dict):
        """

        :param training:
        :param testing:
        :param arguments:
        """

        self.__training = training
        self.__testing = testing
        self.__arguments = arguments

    def __get_data(self, code: str) -> pd.DataFrame:
        """

        :param code:
        :return:
        """

        frame: pd.DataFrame = self.__training.loc[self.__training['hospital_code'] == code, :]
        frame.sort_values(by=['week_ending_date'], ascending=True, inplace=True)

        return frame

    def exc(self):

        algorithm = src.modelling.algorithm.Algorithm(arguments=self.__arguments)
        forecasting = src.modelling.forecasting.Forecasting(arguments=self.__arguments)

        for code in self.__training['hospital_code'].unique():

            data = self.__get_data(code=code)
            model, details = algorithm.exc(data=data)
            predictions = forecasting.exc(model=model, details=details)
