import arviz

import pandas as pd
import numpy as np

import config

class Interface:

    def __init__(self, idata: arviz.data.InferenceData, n_samples: int):
        """

        :param idata:
        :param n_samples:
        """

        self.__idata = idata
        self.__n_samples = n_samples

        # Posteriors
        self.__posteriors = self.__idata['posterior'].stack(sample=('chain', 'draw'))

        # Configurations
        self.__configurations = config.Config()
        self.__rng = np.random.default_rng(self.__configurations.seed)

    def __indices(self) -> np.ndarray:

        chains = self.__idata['sample_stats'].sizes['chain']
        draws = self.__idata['sample_stats'].sizes['draw']

        return self.__rng.integers(chains*draws, size=self.__n_samples)

    def __lag_coefficients(self, code: str, indices: np.ndarray) -> np.ndarray:

        d_lc = self.__posteriors[f'lag_coefficients_{code}'].values.T[indices].T
        d_lc = np.moveaxis(d_lc, 2, 0)
        d_lc = np.moveaxis(d_lc, -1, 1)
        d_lc = np.expand_dims(d_lc, axis=3)

        return d_lc

    def exc(self, data: pd.DataFrame):

        # The hospital/institution codes
        codes = data['hospital_code'].unique()

        indices = self.__indices()
        for code in codes:

            points = data.copy().loc[data['hospital_code'] == code, ['d_of_ln']]

            d_intercept = self.__posteriors[f'alpha_{code}'].values.T[indices]


