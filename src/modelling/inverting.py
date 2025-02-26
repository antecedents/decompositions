import pandas as pd
import numpy as np

class Inverting:

    def __init__(self, master: pd.DataFrame, arguments: dict):

        self.__master = master
        self.__arguments = arguments

    def __indices(self):

        return self.__master.index.append(
            pd.date_range(start=self.__master.index.max(), periods=self.__arguments['ahead'] + 1,
                          freq='W', inclusive='right'))

    def __invert(self, values: np.ndarray):

        # Append estimates
        starting: np.ndarray = self.__master['dt'].to_numpy()
        points = np.concatenate((starting, values))
