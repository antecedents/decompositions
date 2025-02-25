"""Module interface.py"""
import logging

import boto3
import pandas as pd

import src.modelling.splits
import src.s3.configurations


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

    def __arguments(self) -> dict:
        """

        :return:
        """

        return src.s3.configurations.Configurations(connector=self.__connector).objects(
            key_name=('architecture' + 'single' + '/' + 'difference' + 'arguments.json')
        )

    def exc(self, data: pd.DataFrame):
        """

        :return:
        """

        arguments = self.__arguments()

        # Splits
        training, testing = src.modelling.splits.Splits(data=data).exc()
