"""Module autoregression.py"""
import logging
import pymc


class Autoregression:
    """
    A helper that constructs the autoregressive step for the marginal contribution of each lagged
    term, of each time series equation.
    """

    def __init__(self):
        """
        Constructor
        """

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')

        self.__logger = logging.getLogger(__name__)

    @staticmethod
    def exc(lag_coefficients, n_equations, n_lags, blob):
        """

        :param lag_coefficients: pymc.Normal
        :param n_equations: np.int
        :param n_lags: np.int
        :param blob: pandas.DataFrame
        :return:
        """

        steps = []
        for j in range(n_equations):
            ar = pymc.math.sum(
                [
                    pymc.math.sum(lag_coefficients[j, i] * blob.values[n_lags - (i + 1) : -(i + 1)], axis=-1)
                    for i in range(n_lags)
                ],
                axis=0,
            )
            steps.append(ar)
        beta = pymc.math.stack(steps, axis=-1)

        return beta
