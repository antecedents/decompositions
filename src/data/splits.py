"""Module splits.py"""
import logging

import dask
import numpy as np
import pandas as pd

import config
import src.functions.streams


class Splits:
    """
    The original data, and the training & test splits
    """

    def __init__(self, data: pd.DataFrame):
        """

        :param data:
        """

        self.__frame = data.copy()

        # Instances
        self.__configurations = config.Config()
        self.__streams = src.functions.streams.Streams()

    def __persist(self, blob: pd.DataFrame, path: str) -> str:
        """

        :param blob: The data to be stored.
        :param path: Data storage path, including a file name, and extension.
        :return:
        """

        return self.__streams.write(blob=blob, path=path)

    @dask.delayed
    def __data(self, code: str):
        """

        :param code:
        :return:
        """

        blob = self.__frame.copy().loc[self.__frame['hospital_code'] == code, :]

        # Exclude NaN instances vis-a-vis `d_of_ln`
        blob: pd.DataFrame = blob.copy().loc[blob['d_of_ln'].notna(), :]
        blob.sort_values(by='week_ending_date', ascending=True, inplace=True)

        return blob

    @dask.delayed
    def __include(self, blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param blob:
        :return:
        """

        return blob.copy()[:-self.__configurations.ahead]

    @dask.delayed
    def __exclude(self, blob: pd.DataFrame) -> pd.DataFrame:
        """
        Excludes instances that will be predicted

        :param blob:
        :return:
        """

        return blob.copy()[-self.__configurations.ahead:]

    def exc(self):
        """

        :return:
        """

        codes = self.__frame['hospital_code'].unique()

        computations = []
        for code in codes:
            blob = self.__data(code=code)
            include = self.__include(blob=blob)
            exclude = self.__exclude(blob=blob)
            computations.append([include, exclude])
        calculations = dask.compute(computations, scheduler='threads')[0]
        logging.info(calculations)

        including = [calculations[i][0] for i in range(len(calculations))]
        excluding = [calculations[i][1] for i in range(len(calculations))]
        logging.info(pd.concat(including, axis=0, ignore_index=True))
        logging.info(pd.concat(excluding, axis=0, ignore_index=True))
