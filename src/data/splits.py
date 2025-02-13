"""Module splits.py"""
import logging
import os
import typing

import dask
import pandas as pd

import config
import src.functions.directories
import src.functions.streams


class Splits:
    """
    The original data, and the training & test splits
    """

    def __init__(self, data: pd.DataFrame, stamp: str):
        """

        :param data:
        :param stamp:
        """

        self.__frame = data.copy()
        self.__stamp = stamp

        # Instances
        self.__configurations = config.Config()
        self.__directories = src.functions.directories.Directories()
        self.__streams = src.functions.streams.Streams()

    def __persist(self, blob: pd.DataFrame, name: str) -> None:
        """

        :param blob: The data to be stored.
        :param name: A file name, excluding its extension.
        :return:
        """

        path = os.path.join(self.__configurations.artefacts_, self.__stamp, 'data', f'{name}.csv')
        message = self.__streams.write(blob=blob, path=path)
        logging.info(message)

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

    def exc(self) -> typing.Tuple[pd.DataFrame, pd.DataFrame]:
        """

        :return:
        """

        codes = self.__frame['hospital_code'].unique()

        # Splitting by institution
        computations = []
        for code in codes:
            blob = self.__data(code=code)
            include = self.__include(blob=blob)
            exclude = self.__exclude(blob=blob)
            computations.append([include, exclude])
        calculations = dask.compute(computations, scheduler='threads')[0]

        # Structure
        including = [calculations[i][0] for i in range(len(calculations))]
        excluding = [calculations[i][1] for i in range(len(calculations))]
        training = pd.concat(including, axis=0, ignore_index=True)
        testing = pd.concat(excluding, axis=0, ignore_index=True)

        # Persist
        self.__persist(blob=training, name='training')
        self.__persist(blob=testing, name='testing')

        return training, testing
