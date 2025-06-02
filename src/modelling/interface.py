"""Module interface.py"""
import logging

import pandas as pd

import config
import src.elements.codes as ce
import src.functions.directories
import src.modelling.initial


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

        # Instances
        self.__configurations = config.Config()
        self.__directories = src.functions.directories.Directories()

    def exc(self, codes: list[ce.Codes]) -> list[str]:
        """
        Each instance of codes consists of the health board & institution/hospital codes of an institution/hospital.
        
        :return: 
        """

        # Seasonal Component Modelling
        messages = src.modelling.initial.Initial(
            data=self.__data, codes=codes, arguments=self.__arguments).exc()

        return messages
