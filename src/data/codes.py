"""Module codes.py"""
import pandas as pd

import src.elements.codes as ce


class Codes:
    """
    Determines the unique set of health board & institution pairings
    """

    def __init__(self):
        pass

    @staticmethod
    def __structure(values: list[dict]) -> list[ce.Codes]:
        """

        :param values:
        :return:
        """

        return [ce.Codes(**value) for value in values]

    def exc(self, doublet: pd.DataFrame) -> list[ce.Codes]:
        """

        :param doublet: Distinct pairings of board & institution codes
        :return:
        """

        values: list[dict] = doublet.copy().reset_index(drop=True).to_dict(orient='records')

        return self.__structure(values=values)
