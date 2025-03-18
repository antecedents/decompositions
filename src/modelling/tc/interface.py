"""Module interface.py"""
import logging
import os

import arviz
import pandas as pd

import config
import src.functions.streams
import src.modelling.tc.algorithm
import src.modelling.tc.dates
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
        self.__dates = src.modelling.tc.dates.Dates()

    @staticmethod
    def __persist_inference_data(data: arviz.InferenceData, name: str) -> None:
        """

        :param data: The inference data, after the modelling step
        :param name: A <i>directory + file name + file extension</i> for inference data storage
        :return:
        """

        code = os.path.basename(os.path.dirname(name))

        try:
            data.to_netcdf(filename=name)
            logging.info('%s: %s succeeded', code, os.path.basename(name))
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
        dates = self.__dates.exc(training=training, ahead=self.__arguments.get('ahead'))
        model, details, forecasts  = src.modelling.tc.algorithm.Algorithm(
            training=training, dates=dates, arguments=self.__arguments).exc()
        logging.info('Ending trend component modelling phase: %s', institution)

        # Persist: Path
        path = os.path.join(self.__configurations.artefacts_, 'models', institution)

        # ... architecture
        src.modelling.tc.page.Page(
            model=model, path=path).exc(label='algorithm')

        # ... inference
        self.__persist_inference_data(
            data=details, name=os.path.join(path, 'tcf_details.nc'))

        # ... lean predictions
        src.functions.streams.Streams().write(
            blob=forecasts, path=os.path.join(path, 'tcf_forecasts.csv'))

        return f'Trend Component Modelling: Success -> {institution}'
