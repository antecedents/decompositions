"""Module informatics.py"""
import logging

import arviz
import arviz.data
import pymc


class Informatics:
    """
    Class Informatics
    """

    def __init__(self):
        """
        Constructor
        """

        # These are regex strings for the members of <model.named_vars>
        self.__variables = ['alpha_*', 'beta_*', 'lc_*', 'beta_x_*', 'sigma_*', 'likelihood_*']

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __summary(self, idata: arviz.data.InferenceData):
        """

        :param idata:
        :return:
        """

        for variable in self.__variables:

            self.__logger.info(
                arviz.summary(data=idata, var_names=[variable], filter_vars='regex'))

    def exc(self, model: pymc.model.core.Model, idata: arviz.data.InferenceData):
        """

        :param model:
        :param idata:
        :return:
        """

        self.__logger.info(model)
        self.__logger.info(idata)
