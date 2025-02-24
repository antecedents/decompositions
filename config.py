"""
Module config.py
"""
import datetime
import os


class Config:
    """
    Description
    -----------

    A class for configurations
    """

    def __init__(self) -> None:
        """
        Notes<br>
        -------<br>

        <a href="https://otexts.com/fpp2/stationarity.html">Stationarity</a>
        """

        self.warehouse = os.path.join(os.getcwd(), 'warehouse')
        self.artefacts_ = os.path.join(self.warehouse, 'artefacts')

        # Configuration files
        self.s3_parameters_key = 's3_parameters.yaml'

        # Fields
        self.fields = ['week_ending_date', 'health_board_code', 'hospital_code', 'n_attendances']

        # Cut-off, boundary.
        self.boundary = '2020-06-01'

        # Date Stamp: The most recent Tuesday.  The code of Tuesday is 1, hence now.weekday() - 1
        now = datetime.datetime.now()
        offset = (now.weekday() - 1) % 7
        tuesday = now - datetime.timedelta(days=offset)
        self.stamp = tuesday.strftime('%Y-%m-%d')
