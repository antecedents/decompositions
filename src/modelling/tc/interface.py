"""Module interface.py"""
import logging
import os

import arviz
import pandas as pd

import config
import src.functions.streams
import src.modelling.tc.algorithm
import src.modelling.tc.page


class Interface:
    """
    The trend component modelling interface
    """

    def __init__(self, arguments: dict):
        """

        :param arguments:
        """

        self.__arguments = arguments

        # Configurations
        self.__configurations = config.Config()

    @staticmethod
    def __persist_inference_data(data: arviz.InferenceData, name: str) -> str:
        """

        :param data: The inference data, after the modelling step
        :param name: A <i>directory + file name + file extension</i> for inference data storage
        :return:
        """

        try:
            data.to_netcdf(filename=name)
            return os.path.basename(name)
        except IOError as err:
            raise err from err

    def exc(self, training: pd.DataFrame) -> str:
        """

        :param training: The training data of an institution.
        :return:
        """

        institution: str = training['hospital_code'].values[0]
        logging.info('Starting trend component modelling phase: %s', institution)

        # Model, etc.
        model, details, forecasts  = src.modelling.tc.algorithm.Algorithm(
            training=training, arguments=self.__arguments).exc()
        logging.info('End of trend component modelling phase: %s', institution)

        # Persist: Path
        path = os.path.join(self.__configurations.artefacts_, 'models', institution)

        # ... architecture
        src.modelling.tc.page.Page(
            model=model, path=path).exc(label='algorithm')

        # ... inference
        message = self.__persist_inference_data(
            data=details, name=os.path.join(path, f'tcf_details.nc'))
        logging.info('%s: succeeded (%s)', message, institution)

        # ... lean predictions
        message = src.functions.streams.Streams().write(
            blob=forecasts, path=os.path.join(path, 'tcf_forecasts.csv'))
        logging.info('%s (%s)', message, institution)

        return f'Trend Component Modelling: Success -> {institution}'
