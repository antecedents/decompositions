import os
import pymc

import config

class Architecture:

    def __init__(self, stamp: str):
        """
        
        :param stamp:
        """

        self.__stamp = stamp

        # Configurations
        self.__configurations = config.Config()

    def exc(self, model: pymc.model.core.Model, board: str):
        """

        :param model: The estimated model
        :param board: A health board
        :return:
        """

        pathstr = os.path.join(
            self.__configurations.artefacts_, self.__stamp, 'architecture', f'{board}.pdf')

        pymc.model_to_graphviz(model, save=pathstr, figsize=(5,5))
