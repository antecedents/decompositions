import logging
import pymc
import arviz
import arviz.data


class Informatics:

    def __init__(self):

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __summary(self, idata: arviz.data.InferenceData):

        self.__logger.info(arviz.summary(data=idata, var_names=['alpha*']))

    def exc(self, model: pymc.model.core.Model, idata: arviz.data.InferenceData):

        self.__logger.info(model.named_vars)
        self.__logger.info(idata)
