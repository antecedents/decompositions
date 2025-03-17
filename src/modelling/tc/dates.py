"""Module dates.py"""
import numpy as np
import pandas as pd


class Dates:
    """
    <b>Notes</b><br>
    ------<br>

    Creates an array of dates vis-à-vis (a) the training data, (b) the testing data, and
    (c) predictions beyond the testing data dates.<br>
    """

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

        :param training: The training data of an institution
        :param ahead: Forecasting steps ahead; the ahead value is used to
                      split the data into training and testing parts.  The project
                      forecasts $2 * ahead$ steps ahead; the true values of the last set of
                      ahead points will be known in future.
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
