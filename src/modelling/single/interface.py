import pandas as pd

class Interface:

    def __init__(self, training: pd.DataFrame):

        self.__training = training

    def __get_data(self, code: str) -> pd.DataFrame:
        """

        :param code:
        :return:
        """

        frame: pd.DataFrame = self.__training.loc[self.__training['hospital_code'] == code, :]
        frame.sort_values(by=['week_ending_date'], ascending=True, inplace=True)

        return frame

    def exc(self):
        pass