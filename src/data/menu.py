"""Module menu.py"""
import logging
import os

import pandas as pd

import config
import src.functions.objects


class Menu:
    """
    Menu
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

    def exc(self, reference: pd.DataFrame):
        """

        :param reference: A reference sheet.
        :return:
        """

        # Sort
        excerpt = reference.copy().sort_values(by=['health_board_name', 'hospital_name'], ascending=True)

        # Nodes
        names = (excerpt['hospital_name'] + '/' + excerpt['health_board_name']).to_numpy()
        frame = pd.DataFrame(data={'desc': excerpt['health_board_code'].to_numpy(),
                                   'name': names})
        nodes = frame.to_dict(orient='records')
        logging.info(nodes)

        # Persist
        message = src.functions.objects.Objects().write(
            nodes=nodes, path=os.path.join(self.__configurations.menu_, 'menu.json'))
        logging.info('Graphing Menu ->\n%s', message)
