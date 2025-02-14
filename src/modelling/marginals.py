
import pymc
import pytensor
import pandas as pd

class Marginals:
    """
    Computing auto regressive steps
    """

    def __init__(self):
        pass

    @staticmethod
    def exc(lag_coefs: pytensor.tensor.TensorVariable, n_eqs: int, n_lags: int, df: pd.DataFrame):

        ars = []
        for j in range(n_eqs):
            ar = pymc.math.sum(
                [
                    pymc.math.sum(lag_coefs[j, i] * df.values[n_lags - (i + 1) : -(i + 1)], axis=-1)
                    for i in range(n_lags)
                ],
                axis=0,
            )
            print(ar)
            ars.append(ar)
        beta = pymc.math.stack(ars, axis=-1)

        return beta
