"""Module interface.py"""
import logging
import boto3

import pandas as pd

import config
import src.modelling.splits


class Interface:
    """
    Interface
    """

    def __init__(self, connector: boto3.session.Session, stamp: str):
        """

        :param stamp:
        """

        self.__connector = connector
        self.__stamp = stamp

        # Configurations, etc
        self.__configurations = config.Config()

    def exc(self, data: pd.DataFrame):
        """

        :return:
        """

        # Splits
        training, testing = src.modelling.splits.Splits(data=data).exc()


