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
        self.data_ = os.path.join(os.getcwd(), 'data')

        # Cut-off, boundary, for modelling; additionally the number of last time points to exclude.
        self.boundary = '2020-06-01'
        self.exclude = 6

        # Seed
        self.seed = 5

        # Configuration files
        self.s3_parameters_key = 's3_parameters.yaml'

        # For architecture JSON
        self.seasons = 52
        self.trends = 1
