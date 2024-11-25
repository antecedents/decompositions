import logging
import urllib.request
import json
import pandas as pd

class Data:

    def __init__(self) -> None:
        
        self.__url = 'https://www.opendata.nhs.scot/api/3/action/datastore_search?resource_id=a5f7ca94-c810-41b5-a7c9-25c18d43e5a4&limit=1000000'

        self.__rename = {
            'WeekEndingDate': 'week_ending_date', 'HBT': 'health_board_code', 'TreatmentLocation': 'treatment_location', 
            'NumberOfAttendancesEpisode': 'n_attendances', 'NumberWithin4HoursEpisode': 'n_within_4_hours', 
            'NumberOver4HoursEpisode': 'n_over_4_hours', 'NumberOver8HoursEpisode': 'n_over_8_hours', 
            'NumberOver12HoursEpisode': 'n_over_12_hours'}

    def __get_data(self):

        fileobj = urllib.request.urlopen(url=self.__url)
        objects = fileobj.read()
        dictionary = json.loads(s=objects)

        readings = pd.DataFrame.from_dict(data=dictionary['result']['records'], orient='columns')

        return readings

    def __inspect(self, blob: pd.DataFrame):

        readings = blob.copy()

        details = blob['DepartmentType'].unique()
        logging.info(details)
        logging.info(type(details))

    def __structure(self, blob: pd.DataFrame):

        readings = blob.copy()[[
            'WeekEndingDate', 'HBT', 'TreatmentLocation', 'NumberOfAttendancesEpisode', 'NumberWithin4HoursEpisode',
            'NumberOver4HoursEpisode', 'NumberOver8HoursEpisode', 'NumberOver12HoursEpisode']]

        readings.rename(columns=self.__rename, inplace=True)

        readings['week_ending_date'] = pd.to_datetime(
            readings['week_ending_date'].astype(dtype=str), errors='coerce', format='%Y%m%d')

        return readings

    def exc(self):

        data = self.__get_data()
        self.__inspect(blob=data)
        data = self.__structure(blob=data)
        logging.info(data.head())
        
        return data
