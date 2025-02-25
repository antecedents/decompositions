"""Module algorithm.py"""
import typing

import numpy as np
import pandas as pd
import pymc
import pymc.sampling.jax

import config
import src.modelling.marginals


class Algorithm:
    """
    The multi-level algorithm
    """

    def __init__(self) -> None:
        """
        Constructor
        """

        self.__configurations = config.Config()
        self.__marginals = src.modelling.marginals.Marginals()

    def exc(self, n_lags: int, n_equations: int, data: pd.DataFrame, leaves: str, prior_checks: bool = False):
        """

        :param n_lags: <br># of non-constant coefficients<br>
        :param n_equations: <br># of independent variables.  Beware, this algorithm is inappropriate for cases whereby
                      there are two or more variates because it does not consider multi-variate covariance.<br>
        :param data: <br>The training data of a board; a board consists of one or more hospitals/institutions.<br>
        :param leaves: <br>The field that identifies an instance's group<br>
        :param prior_checks: <br>Focusing on priors only?<br>
        :return:
        """

        cols = [col for col in data.columns if col != leaves]
        coords = {'lags': np.arange(n_lags) + 1,
                  'equations': cols}

        groups = data[leaves].unique()

        with pymc.Model(coords=coords) as model:

            pass
