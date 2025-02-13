import os

import dask
import numpy as np
import pandas as pd

import config
import src.functions.directories
import src.functions.streams


class Features:

    def __init__(self, data: pd.DataFrame, stamp: str):
        """

        :param data: The data.
        :param stamp: Date Stamp
        """

        self.__data = data.copy()
        self.__stamp = stamp

        # Configurations
        self.__configurations = config.Config()
        
    def __persist(self, blob: pd.DataFrame) -> str:
        
        pathstr = os.path.join(self.__configurations.artefacts_, self.__stamp, 'data', 'data.csv')

        # Ascertain the existence of the target directory, then save.
        src.functions.directories.Directories().create(path=os.path.dirname(pathstr))

        return src.functions.streams.Streams().write(blob=blob, path=pathstr)

    @dask.delayed
    def __features(self, code: str):
        """

        :param code:
        :return:
        """

        blob = self.__data.copy().loc[self.__data['hospital_code'] == code, :]

        blob['ln'] = np.log(blob['n_attendances'].to_numpy())
        blob['d_of_ln'] = blob['ln'].diff(periods=self.__configurations.seasons)
        blob['d_of_ln'] = blob['d_of_ln'].diff(periods=self.__configurations.trends)

        # Sort
        blob.sort_values(by='week_ending_date', ascending=True, inplace=True)

        return blob

    def exc(self) -> pd.DataFrame:
        """

        :return:
        """

        # The
        codes = self.__data['hospital_code'].unique()

        computations = []
        for code in codes:
            computations.append(self.__features(code=code))
        calculations = dask.compute(computations, scheduler='threads')[0]

        frame = pd.concat(calculations, axis=0, ignore_index=True)

        return frame
