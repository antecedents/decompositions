import logging
import os
import boto3
import pytensor
import numpyro
import jax
import typing


import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.environment
import src.data.interface
import src.functions.cache
import src.functions.service
import src.modelling.interface
import src.s3.s3_parameters
import src.s3.configurations
import src.setup
import src.transfer.interface

class Interface:

    def __init__(self):

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')

        self.__logger: logging.Logger = logging.getLogger(__name__)

    @staticmethod
    def __compute(arguments: dict):

        jax.config.update('jax_platform_name', 'cpu')
        jax.config.update('jax_enable_x64', True)

        numpyro.set_platform('cpu')
        numpyro.set_host_device_count(os.cpu_count())

        src.environment.Environment(arguments=arguments)

    @staticmethod
    def __setting_up(service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service:
        :param s3_parameters:
        :return:
        """

        # Setting up
        src.setup.Setup(service=service, s3_parameters=s3_parameters).exc()

    def exc(self) -> typing.Tuple[boto3.session.Session, s3p.S3Parameters, sr.Service, dict]:
        """

        :return:
        """

        connector = boto3.session.Session()
        s3_parameters: s3p.S3Parameters = src.s3.s3_parameters.S3Parameters(connector=connector).exc()
        service: sr.Service = src.functions.service.Service(connector=connector, region_name=s3_parameters.region_name).exc()

        arguments: dict = src.s3.configurations.Configurations(connector=connector).objects(
            key_name=('artefacts' + '/' + 'architecture' + '/' + 'single' + '/' + 'futures' + '/' + 'arguments.json'))

        pytensor.config.blas__ldflags = '-llapack -lblas -lcblas'
        self.__compute(arguments=arguments)
        self.__setting_up(service=service, s3_parameters=s3_parameters)

        self.__logger.info('BLAS: %s', pytensor.config.blas__ldflags)

        return connector, s3_parameters, service, arguments
