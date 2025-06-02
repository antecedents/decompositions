"""Module initial.py"""
import dask
import pandas as pd

import src.algorithms.decompose
import src.algorithms.persist
import src.elements.specifications as se
import src.functions.directories


class Initial:
    """
    Seasonal component modelling.
    """

    def __init__(self, data: pd.DataFrame, specifications_: list[se.Specifications], arguments: dict):
        """

        :param data: The weekly accidents & emergency data of institutions/hospitals
        :param specifications_: The unique set of health board & institution pairings.
        :param arguments: A set of model development, and supplementary, arguments.
        """

        self.__data = data
        self.__specifications_ = specifications_
        self.__arguments = arguments

    @dask.delayed
    def __get_data(self, specifications: se.Specifications) -> pd.DataFrame:
        """

        :param specifications: The board & institution codes, etc.
        :return:
        """

        frame = self.__data.copy().loc[self.__data['hospital_code'] == specifications.hospital_code, :]
        frame.set_index(keys='week_ending_date', drop=True, inplace=True)
        frame.sort_values(by=['week_ending_date'], ascending=True, ignore_index=False, inplace=True)

        return frame

    def exc(self) -> list[str]:
        """

        :return:
        """

        # Additional delayed tasks
        __decompose = dask.delayed(src.algorithms.decompose.Decompose(arguments=self.__arguments).exc)
        __persist = dask.delayed(src.algorithms.persist.Persist().exc)

        computations = []
        for specifications in self.__specifications_:
            data: pd.DataFrame = self.__get_data(specifications=specifications)
            decompositions = __decompose(data=data)
            message = __persist(decompositions=decompositions, specifications=specifications)
            computations.append(message)
        messages = dask.compute(computations, scheduler='threads')[0]

        return messages
