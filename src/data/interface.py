"""Module interface.py"""
import os
import typing
import pandas as pd

import config
import src.elements.s3_parameters as s3p
import src.elements.text_attributes as txa
import src.functions.streams
import src.data.features
import src.data.splits


class Interface:
    """
    Notes<br>
    ------<br>

    Reads-in the data in focus.
    """

    def __init__(self, s3_parameters: s3p.S3Parameters, arguments: dict):
        """

        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        :param arguments:
        """

        self.__s3_parameters = s3_parameters
        self.__arguments = arguments

        # Configurations
        self.__configurations = config.Config()

        # The data sets' uniform resource identifier
        self.__uri = ('s3://' + self.__s3_parameters.internal + '/' +
               self.__s3_parameters.path_internal_data + f'raw/{self.__configurations.stamp}.csv')

        # Storage
        self.__storage: str = os.path.join(self.__configurations.artefacts_, self.__configurations.stamp, 'data')

        # Instances
        self.__streams = src.functions.streams.Streams()

    def __get_data(self) -> pd.DataFrame:
        """

        :return:
        """

        text = txa.TextAttributes(uri=self.__uri, header=0)
        frame = self.__streams.read(text=text)
        frame['week_ending_date'] = pd.to_datetime(
            frame['week_ending_date'].astype(dtype=str), errors='coerce', format='%Y-%m-%d')

        return frame[self.__configurations.fields]

    def __persist(self, blob: pd.DataFrame, name: str) -> str:
        """

        :param blob:
        :param name:
        :return:
        """

        return src.functions.streams.Streams().write(
            blob=blob, path=os.path.join(self.__storage, f'{name}.csv'))

    def exc(self) -> typing.Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """

        :return:
        """

        # The data
        data = self.__get_data()

        # Features, Splits
        data = src.data.features.Features(data=data.copy(), arguments=self.__arguments).exc()
        training, testing = src.data.splits.Splits(data=data.copy(), arguments=self.__arguments).exc()

        return data, training, testing
