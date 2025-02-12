"""Module splits.py"""
import pandas as pd

import src.functions.streams

class Splits:
    """
    The original data, and the training & test splits
    """

    def __init__(self):
        """
        Constructor
        """


        self.__streams = src.functions.streams.Streams()

    def __persist(self, blob: pd.DataFrame, path: str) -> str:
        """

        :param blob: The data to be stored.
        :param path: Data storage path, including a file name, and extension.
        :return:
        """

        return self.__streams.write(blob=blob, path=path)
