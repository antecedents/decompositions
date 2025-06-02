"""Module specifications.py"""
import pandas as pd

import src.elements.specifications as se


class Specifications:
    """
    Creates an attributes collection per gauge
    """

    def __init__(self):
        pass

    @staticmethod
    def exc(reference: pd.DataFrame) -> list[se.Specifications]:
        """

        :param reference:
        :return:
        """

        dictionaries = [reference.iloc[i, :].squeeze() for i in range(reference.shape[0])]
        specifications_ = [se.Specifications(**dictionary) for dictionary in dictionaries]

        return specifications_
