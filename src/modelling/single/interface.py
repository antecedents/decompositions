import boto3
import pandas as pd

import src.s3.configurations


class Interface:

    def __init__(self, connector: boto3.session.Session, training: pd.DataFrame):
        """

        :param connector:
        :param training:
        """

        self.__connector = connector
        self.__training = training

    def __get_data(self, code: str) -> pd.DataFrame:
        """

        :param code:
        :return:
        """

        frame: pd.DataFrame = self.__training.loc[self.__training['hospital_code'] == code, :]
        frame.sort_values(by=['week_ending_date'], ascending=True, inplace=True)

        return frame

    def __arguments(self) -> dict:
        """

        :return:
        """

        return src.s3.configurations.Configurations(connector=self.__connector).objects(
            key_name=('architecture' + '/' + 'single' + '/' + 'difference' + '/' + 'arguments.json')
        )


    def exc(self):

        arguments = self.__arguments()