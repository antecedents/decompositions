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
        
        self.seed = 5

        # Configuration files
        self.s3_parameters_key = 's3_parameters.yaml'
