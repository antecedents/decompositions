"""Module interface.py"""
import pandas as pd

import src.modelling.temporary


class Interface:
    """
    Interface
    """

    def __init__(self):
        pass

    @staticmethod
    def exc():
        """

        :return:
        """

        temporary: pd.DataFrame = src.modelling.temporary.Temporary().exc()
