"""Module temporary.py"""
import os

import numpy as np
import pandas as pd

import config
import src.elements.text_attributes as txa
import src.functions.streams


class Temporary:
    """
    Temporary
    """

    def __init__(self):
        """
        Constructor
        """

        self.__streams = src.functions.streams.Streams()
        self.__configurations = config.Config()

    def __get_data(self) -> pd.DataFrame:
        """

        :return:
        """

        text = txa.TextAttributes(uri=os.path.join(self.__configurations.data_, 'data.csv'), header=0)
        data = self.__streams.read(text=text)

        data['week_ending_date'] = pd.to_datetime(
            data['week_ending_date'].astype(dtype=str), errors='coerce', format='%Y-%m-%d')

        return data

    def __excerpt(self, blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param blob:
        :return:
        """

        return blob.loc[blob['week_ending_date'] > np.datetime64(self.__configurations.boundary), :]

    def exc(self):
        """

        :return:
        """

        data = self.__get_data()
        data = self.__excerpt(blob=data.copy())

        return data
