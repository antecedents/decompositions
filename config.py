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
        #   independent variables: In this context, `n_attendances` only
        # And more.
        self.n_lags = 52
        self.n_equations = 1
        self.group_field = 'hospital_code'

        # Cut-off, boundary.
        self.boundary = '2020-06-01'

        # Priors
        self.priors = {
            'alpha_hat_location': {'mu': 0, 'sigma': 0.1},
            'alpha_hat_scale': {'alpha': 3, 'beta': 0.5},
            'beta_hat_location': {'mu': 0, 'sigma': 0.1},
            'beta_hat_scale': {'alpha': 3, 'beta': 0.5},
            'z_scale_alpha': {'alpha': 3, 'beta': 0.5},
            'z_scale_beta': {'alpha': 3, 'beta': 0.5},
            'noise': {'sigma': 1}
        }
