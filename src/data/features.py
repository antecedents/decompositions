import pandas as pd
import numpy as np

import dask

import config


class Features:

    def __init__(self, data: pd.DataFrame):
        """

        :param data:
        """

        self.__frame = data.copy()

        # Configurations
        self.__configurations = config.Config()

    @dask.delayed
    def __features(self, code: str):
        """

        :param code:
        :return:
        """

        blob = self.__frame.copy().loc[self.__frame['hospital_code'] == code, :]

        blob['ln'] = np.log(blob['n_attendances'].to_numpy())
        blob['d_of_ln'] = blob['ln'].diff(periods=self.__configurations.seasons)
        blob['d_of_ln'] = blob['d_of_ln'].diff(periods=self.__configurations.trends)

        # Sort
        blob.sort_values(by='week_ending_date', ascending=True, inplace=True)

        return blob

    def exc(self):

        codes = self.__frame['hospital_code'].unique()

        computations = []
        for code in codes:
            computations.append(self.__features(code=code))
        calculations = dask.compute(computations, scheduler='threads')[0]

        pd.concat(calculations, axis=0, ignore_index=True)
