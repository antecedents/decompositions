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

    def exc(self, model: pymc.model.core.Model, stamp: str, name: str):
        """

        :param model: The estimated model
        :param stamp:
        :param name:
        :return:
        """

        pathstr = os.path.join(
            self.__configurations.artefacts_, stamp, 'architecture', f'{name}.pdf')

        pymc.model_to_graphviz(model, save=pathstr, figsize=(5,5))
