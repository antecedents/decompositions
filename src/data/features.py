import pandas as pd


class Features:

    def __init__(self, data: pd.DataFrame):
        """

        :param data:
        """

        self.__frame = data.copy()

    def __data(self):
        pass

    def exc(self):

        codes = self.__frame['hospital_code'].unique()

        computations = []
        for code in codes:
            pass
