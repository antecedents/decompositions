"""
Module config.py
"""
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

        # Seed
        self.seed = 5

        # Configuration files
        self.s3_parameters_key = 's3_parameters.yaml'

        '''
        For architecture JSON
        '''

        # Fields
        self.fields = ['week_ending_date', 'health_board_code', 'hospital_code',  'n_attendances']

        # Seasons, trends, forecast weeks ahead, etc.
        self.seasons = 52
        self.trends = 1
        self.ahead = 9

        # The number of
        #   lags: via partial auto-correlation function of a series that has undergone (a) ln, (b) season
        #         differencing, (c) trend differencing.
        #   independent variables
        self.n_lags = 52
        self.n_eqs = 1

        # Cut-off, boundary, for modelling; additionally the number of final points to exclude.
        self.boundary = '2020-06-01'
