"""Module algorithm.py"""
import pandas as pd
import pymc


# noinspection PyUnresolvedReferences
class Algorithm:
    """
    The multi-level algorithm
    """

    def __init__(self, frames: pd.DataFrame, n_timings: int) -> None:
        """

        :param frames:
        :param n_timings:
        """

        self.__frames = frames
        self.__groups = self.__frames['treatment_location'].unique()

        # Or, the original time points
        self.__timings = list(range(n_timings))

        # ...
        self.__priors = {
            'coefficients': {'size': 53},
            'sigma': 8,
            'init': {'mu': 0.04, 'sigma': 0.1, 'size': 52},
        }

    def exc(self):
        """

        :return:
        """

        # Initialise the model
        with pymc.Model() as ARMODEL_:
            pass

        # Mutable by default
        ARMODEL_.add_coord('obs_id', self.__timings)

        with ARMODEL_:

            _c_location = pymc.Normal('_c_location', 0, 0.1)
            _c_scale = pymc.InverseGamma('_c_scale', 3, 0.5)

            points = pymc.Data('points', self.__timings, dims='obs_id')

            for group in self.__groups:

                core = self.__frames.copy().loc[self.__frames['treatment_location'] == group, :]
                core.sort_index(ascending=True, ignore_index=False, inplace=True)
                __seq = core['n_difference'].to_numpy()

                # And
                _z_scale = pymc.InverseGamma(f'_z_scale_{group}', 3, 0.5)

                # The data containers
                observations = pymc.Data(f'observations_{group}', __seq, dims='obs_id')

                # Setting priors for each coefficient in the AR process
                coefficients = pymc.Normal(f'coefficients_{group}', mu=_c_location, sigma=(_c_scale*_z_scale),
                                           size=self.__priors['coefficients']['size'])
                sigma = pymc.HalfNormal(f'sigma_{group}', self.__priors['sigma'])

                # Initialisation per ...
                init = pymc.Normal.dist(
                    self.__priors['init']['mu'], self.__priors['init']['sigma'], size=self.__priors['init']['size']
                )

                # Autoregressive process with p lags; lags = self.__priors['coef']['size'] - 1
                process = pymc.AR(
                    f'ar_{group}', coefficients, sigma=sigma, init_dist=init, constant=True,
                    steps=points.eval().shape[0] - (self.__priors['coefficients']['size'] - 1),
                    dims='obs_id')

                # Likelihood
                outcome = pymc.Normal(f'likelihood_{group}', mu=process, sigma=sigma, observed=observations, dims='obs_id')

            # Sampling
            details_ = pymc.sample_prior_predictive()
            details_.extend(pymc.sample(2000, random_seed=100, target_accept=0.95))
            details_.extend(pymc.sample_posterior_predictive(details_))

        return details_, ARMODEL_
