"""
Module objects.py
"""
import json
import pathlib
import sys

import requests


class Objects:
    """
    Class Objects

    Description
    -----------
    This class reads & writes JSON (JavaScript Object Notation) objects
    """

    def __init__(self):
        """
        Constructor
        """

    @staticmethod
    def write(nodes: dict, path: str) -> str:
        """

        :param nodes:
        :param path:
        :return:
        """

        name = pathlib.Path(path).stem

        if not bool(nodes):
            return f'{name}: empty'

        try:
            with open(file=path, mode='w', encoding='utf-8') as disk:
                json.dump(obj=nodes, fp=disk, ensure_ascii=False, indent=4)
            return f'{name}: succeeded'
        except IOError as err:
            raise err from err

    @staticmethod
    def api(url: str) -> dict:
        """

        :param url:
        :return:
        """

        try:
            response = requests.get(url=url, timeout=600)
            response.raise_for_status()
        except requests.exceptions.Timeout as err:
            raise err from err
        except requests.exceptions.HTTPError as err:
            raise err from err
        except Exception as err:
            raise err from err

        if response.status_code == 200:
            return response.json()

        sys.exit(response.status_code)

    @staticmethod
    def read(uri: str) -> dict:
        """

        :param uri:
        :return:
        """

        try:
            with open(file=uri, mode='r', encoding='utf-8') as disk:
                return json.load(fp=disk)
        except ImportError as err:
            raise err from err
