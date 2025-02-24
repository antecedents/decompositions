"""Module marginals.py"""
import pandas as pd
import pymc


class Marginals:
    """
    Computing auto regressive steps
    """

    def __init__(self):
        pass

    @staticmethod
    def exc(lc, n_equations: int, n_lags: int, segment: pd.DataFrame):
        """

        :param lc: Lag coefficients.  A pytensor.tensor.TensorVariable of a pymc distribution
        :param n_equations: Equals the number of independent variables.
        :param n_lags: Equivalent to the number of non-constant coefficients.
        :param segment: The training data.
        :return:
        """

        auto_regressive_steps = []
        for j in range(n_equations):
            ar = pymc.math.sum(
                [
                    pymc.math.sum(lc[j, i] * segment.values[n_lags - (i + 1) : -(i + 1)], axis=-1)
                    for i in range(n_lags)
                ],
                axis=0,
            )
            auto_regressive_steps.append(ar)
        beta = pymc.math.stack(auto_regressive_steps, axis=-1)

        return beta
