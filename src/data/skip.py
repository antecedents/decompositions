"""Module skip.py"""
import pandas as pd


class Skip:
    """
    Filters-out institutions that have zero or negative values
    """

    def __init__(self):
        pass

    @staticmethod
    def __skip(data: pd.DataFrame):
        """

        :param data:
        :return:
        """

        # Counting n_attendances values <= 0 per institution
        cases = data.copy()[['hospital_code', 'n_attendances']].groupby('hospital_code').agg(
            missing=('n_attendances', lambda x: sum(x <= 0)))
        cases.reset_index(drop=False, inplace=True)
        cases: pd.DataFrame = cases.copy().loc[cases['missing'] > 0, :]

        # Skip institutions that have zero or negative values
        if not cases.empty:
            data = data.copy().loc[~data['hospital_code'].isin(cases['hospital_code'].unique()), :]

        return data

    def exc(self, data: pd.DataFrame):
        """

        :param data:
        :return:
        """

        return self.__skip(data=data)
