"""Module interface.py"""
import logging
import os
import typing

import boto3
import jax
import numpyro
import pytensor

import src.data.interface
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.functions.service
import src.preface.setup
import src.s3.configurations
import src.s3.s3_parameters


class Interface:
    """
    Interface
    """

    def __init__(self):
        """
        Constructor
        """

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')

        self.__logger: logging.Logger = logging.getLogger(__name__)

    @staticmethod
    def __get_arguments(connector: boto3.session.Session) -> dict:
        """

        :return:
        """

        key_name = 'artefacts' + '/' + 'architecture' + '/' + 'arguments.json'

        return src.s3.configurations.Configurations(connector=connector).objects(key_name=key_name)

    @staticmethod
    def __compute():
        """

        :return:
        """

        jax.config.update('jax_platform_name', 'cpu')
        jax.config.update('jax_enable_x64', True)

        numpyro.set_host_device_count(os.cpu_count())
        numpyro.set_platform('cpu')

    def __states(self):
        """

        :return:
        """

        self.__logger.info('The number of CPU cores: %s', os.cpu_count())
        self.__logger.info('BLAS: %s', pytensor.config.blas__ldflags)

    @staticmethod
    def __setting_up(service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service:
        :param s3_parameters:
        :return:
        """

        src.preface.setup.Setup(service=service, s3_parameters=s3_parameters).exc()

    def exc(self) -> typing.Tuple[boto3.session.Session, s3p.S3Parameters, sr.Service, dict]:
        """

        :return:
        """

        connector = boto3.session.Session()
        s3_parameters: s3p.S3Parameters = src.s3.s3_parameters.S3Parameters(connector=connector).exc()
        service: sr.Service = src.functions.service.Service(
            connector=connector, region_name=s3_parameters.region_name).exc()
        arguments: dict = self.__get_arguments(connector=connector)

        pytensor.config.blas__ldflags = '-llapack -lblas -lcblas'

        self.__compute()
        self.__states()
        self.__setting_up(service=service, s3_parameters=s3_parameters)

        return connector, s3_parameters, service, arguments
