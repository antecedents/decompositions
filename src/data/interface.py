"""Module interface.py"""
import typing
import datetime

import pandas as pd

import config
import src.elements.s3_parameters as s3p
import src.elements.codes as ce
import src.elements.text_attributes as txa
import src.functions.streams
import src.data.codes
import src.data.reference
import src.data.menu
import src.data.skip


class Interface:
    """
    Notes<br>
    ------<br>

    Reads-in the data in focus.
    """

    def __init__(self, s3_parameters: s3p.S3Parameters, arguments: dict):
        """

        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        :param arguments:
        """

        self.__s3_parameters = s3_parameters
        self.__arguments = arguments

        # Configurations
        self.__configurations = config.Config()

        # An instance for writing/reading CSV (comma-separated values) files
        self.__streams = src.functions.streams.Streams()

    def __get_data(self) -> pd.DataFrame:
        """

        :return:
        """

        uri = ('s3://' + self.__s3_parameters.internal + '/' + self.__s3_parameters.path_internal_data +
               self.__configurations.source)
        text = txa.TextAttributes(uri=uri, header=0)
        data = self.__streams.read(text=text)

        return data[self.__configurations.fields]

    def __date_formatting(self, blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param blob:
        :return:
        """

        boundary = datetime.datetime.strptime(self.__arguments.get('boundary'), '%Y-%m-%d')

        blob['week_ending_date'] = pd.to_datetime(
            blob['week_ending_date'].astype(dtype=str), errors='coerce', format='%Y-%m-%d')

        blob = blob.copy().loc[blob['week_ending_date'] > boundary, :]

        return blob


    def exc(self) -> typing.Tuple[pd.DataFrame, list[ce.Codes]]:
        """

        :return:
        """

        # The data
        data = self.__get_data()
        data = self.__date_formatting(blob=data.copy())

        # Skip institutions that have zero or negative n_attendances values
        data = src.data.skip.Skip().exc(data=data.copy())
        doublet = data[['health_board_code', 'hospital_code']].drop_duplicates()

        # Menu
        reference = src.data.reference.Reference(s3_parameters=self.__s3_parameters).exc(identifiers=doublet['hospital_code'].to_list)
        src.data.menu.Menu().exc(reference=reference)

        # A collection of identification codes
        codes = src.data.codes.Codes().exc(doublet=doublet)

        return data, codes
