
import numpy as np
import pandas as pd

class Dates:

    def __init__(self):
        pass

    @staticmethod
    def __ending(data: pd.DataFrame, ahead: int) -> pd.DataFrame:
        """

        :param data:
        :param ahead:
        :return:
        """

        ending = pd.date_range(
            start=data.index.max(),
            periods=1 + 2*ahead,
            freq=data.index.inferred_freq,
            inclusive='right').to_frame()
        ending.reset_index(drop=True, inplace=True)
        ending.rename(columns={0: 'week_ending_date'}, inplace=True)

        return ending

    def exc(self, training: pd.DataFrame, ahead: int) -> np.ndarray:
        """

        :param training:
        :param ahead:
        :return:
        """

        data = training.copy()

        # The beginning
        starting = data.index.to_frame()
        starting.reset_index(drop=True, inplace=True)

        # The dates vis-à-vis testing and futures
        ending = self.__ending(data=training, ahead=ahead)

        # Altogether
        timings = pd.concat([starting, ending], axis=0, ignore_index=True)

        return timings.to_numpy()
