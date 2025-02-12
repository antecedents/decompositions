
import pandas as pd

class Dates:

    def __init__(self):
        pass


    def exc(self, data: pd.DataFrame):

        frame = data.copy()
        frame['week_ending_date'] = pd.to_datetime(frame['week_ending_date'].astype(dtype=str), errors='coerce', format='%Y%m%d')

        minimum = frame['week_ending_date'].min()
        maximum = frame['week_ending_date'].max()
