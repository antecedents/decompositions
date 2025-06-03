"""Module interface.py"""
import pandas as pd

import src.algorithms.initial
import src.elements.specifications as se


class Interface:
    """
    The interface to the seasonal & trend component modelling steps.
    """

    def __init__(self, data: pd.DataFrame, arguments: dict):
        """

        :param data: The weekly accidents & emergency data of institutions/hospitals
        :param arguments: A set of model development, and supplementary, arguments.
        """

        self.__data = data
        self.__arguments = arguments

    def exc(self, specifications_: list[se.Specifications]) -> list[str]:
        """
        Each instance of codes consists of the board & institution codes of an institution/hospital.
        
        :return: 
        """

        # Seasonal Component Modelling
        messages = src.algorithms.initial.Initial(
            data=self.__data, specifications_=specifications_, arguments=self.__arguments).exc()

        return messages
