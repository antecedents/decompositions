"""Module interface.py"""
import logging
import pandas as pd

import src.modelling.algorithm
import src.modelling.temporary


class Interface:
    """
    Interface
    """

    def __init__(self):
        """

        """

        # Temporarily, read-in the local copy of the Amazon data set.
        self.__temporary: pd.DataFrame = src.modelling.temporary.Temporary().exc()

    def exc(self):
        """

        :return:
        """

        # Initially, focus on ...
        data = self.__temporary
        logging.info(data.head())

        # Hence
        details, ARMODEL = src.modelling.algorithm.Algorithm(
            frames=data, n_timings=data.index.unique().shape[0]).exc()
