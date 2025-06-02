"""Module decompose.py"""
import logging
import os

import numpy as np
import pandas as pd
import statsmodels.tsa.seasonal as stsl

import config


class Decompose:
    """
    Notes<br>
    ------<br>

    This class decomposes the <i># of attendances series</i>.
    """

    def __init__(self, arguments: dict):
        """

        :param arguments: The modelling arguments
        """

        self.__arguments: dict = arguments
        self.__decompose: dict = self.__arguments.get('decompose')

        # The parent path of modelling data
        self.__root = os.path.join(config.Config().decompositions_, 'points')

    def __add_components(self, frame: pd.DataFrame) -> pd.DataFrame:
        """

        :param frame:
        :return:
        """

        components: stsl.DecomposeResult = stsl.STL(
            frame['n_attendances'], period=self.__arguments.get('seasons'),
            seasonal=self.__decompose.get('smoother_seasonal'),
            trend_deg=self.__decompose.get('degree_trend'),
            seasonal_deg=self.__decompose.get('degree_seasonal'),
            robust=True).fit()

        frame['trend'] = components.trend
        frame['residue'] = components.resid
        frame['seasonal'] = components.seasonal

        return frame

    @staticmethod
    def __epoch(frame: pd.DataFrame) -> pd.DataFrame:
        """

        :param frame:
        :return:
        """

        instances = frame.copy()
        instances.reset_index(drop=False, inplace=True)
        instances['milliseconds']  = (
                instances['week_ending_date'].to_numpy().astype(np.int64) / (10 ** 6)
        ).astype(np.longlong)
        instances.sort_values(by='week_ending_date', inplace=True)

        return instances

    def exc(self, data: pd.DataFrame) -> pd.DataFrame:
        """

        :param data:
        :return:
        """

        logging.info(data)

        # Decomposition Components
        frame = self.__add_components(frame=data.copy())
        frame = self.__epoch(frame=frame)

        return frame
