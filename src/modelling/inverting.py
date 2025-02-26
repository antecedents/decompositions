import pandas as pd

class Inverting:

    def __init__(self, master: pd.DataFrame, arguments: dict):

        self.__master = master
        self.__arguments = arguments

    def __times(self):

        times = self.__master.index.append(
            pd.date_range(start=self.__master.index.max(), periods=self.__arguments['ahead'] + 1,
                          freq='W', inclusive='right'))
