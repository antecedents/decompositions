"""Module reference.py"""
import pandas as pd

import src.elements.s3_parameters as s3p
import src.elements.text_attributes as txa
import src.functions.streams


class Reference:
    """
    Reference
    """

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters: The overarching S3 (Simple Storage Service) parameters
                              settings of this project, e.g., region code name, buckets, etc.
        """

        self.__s3_parameters: s3p.S3Parameters = s3_parameters
        self.__endpoint = 's3://' + self.__s3_parameters.internal + '/' + 'references' + '/'

        # An instance for reading & writing CSV (comma-separated values) data
        self.__stream = src.functions.streams.Streams()

    def __get_boards(self):
        """

        :return:
        """

        uri = self.__endpoint + 'boards.csv'
        usecols = ['health_board_code', 'health_board_name']

        text = txa.TextAttributes(uri=uri, header=0, usecols=usecols)

        return self.__stream.read(text=text)

    def __get_institutions(self):
        """

        :return:
        """

        uri = self.__endpoint + 'institutions.csv'
        usecols = ['hospital_code',	'hospital_name', 'post_code', 'health_board_code', 'hscp_code',
                   'council_area', 'intermediate_zone',	'data_zone']
        text = txa.TextAttributes(uri=uri, header=0, usecols=usecols)

        return self.__stream.read(text=text)

    def exc(self, identifiers: list[str]) -> pd.DataFrame:
        """

        :param identifiers:  A list of hospital identification codes
        :return:
        """

        reference = self.__get_institutions().merge(self.__get_boards(), how='left', on='health_board_code')

        return reference.loc[reference['hospital_code'].isin(identifiers), :]
