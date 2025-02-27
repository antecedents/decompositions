"""Module architecture.py"""
import os

import pymc

import config


class Architecture:
    """
    Architecture
    """

    def __init__(self):
        """
        Constructor
        """

        # Configurations
        self.__configurations = config.Config()

    def exc(self, model: pymc.model.core.Model, hospital_code: str):
        """

        :param model: The estimated model
        :param hospital_code:
        :return:
        """

        pathstr = os.path.join(
            self.__configurations.artefacts_models, hospital_code, 'architecture.pdf')

        pymc.model_to_graphviz(model, save=pathstr, figsize=(5,5))
