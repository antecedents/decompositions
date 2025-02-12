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
        Constructor
        """

        self.warehouse = os.path.join(os.getcwd(), 'warehouse')
        self.artefacts_ = os.path.join(self.warehouse, 'artefacts')

        # Cut-off, boundary, for modelling; additionally the number of final points to exclude.
        self.boundary = '2020-06-01'
        self.exclude = 6

        # Seed
        self.seed = 5

        # Configuration files
        self.s3_parameters_key = 's3_parameters.yaml'

        # For architecture JSON
        self.seasons = 52
        self.trends = 1
        self.ahead = 9
