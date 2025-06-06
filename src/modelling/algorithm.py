"""Module algorithm.py"""

import pandas as pd
import statsmodels.tsa.forecasting.stl as tfc

import src.elements.codes as ce
import src.modelling.fundamental
import src.modelling.seasonal


class Algorithm:
    """
    Class Algorithm
    """

    def __init__(self, arguments: dict):
        """

        :param arguments:
        """

        self.__arguments: dict = arguments

    def exc(self, training: pd.DataFrame, code: ce.Codes) -> tfc.STLForecastResults | None:
        """
        <b>References</b><br>
        <a href="https://www.statsmodels.org/dev/generated/statsmodels.tsa.arima.model.ARIMA.html">
        ARIMA (Autoregressive Integrated Moving Average)</a><br>
        <a href="https://www.statsmodels.org/stable/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html">
        SARIMAX (Seasonal AutoRegressive Integrated Moving Average with eXogenous)</a><br>
        <a href="https://www.statsmodels.org/dev/generated/statsmodels.tsa.forecasting.stl.STLForecast.html">
        STLForecast</a><br><br>

        :param training: The data of an institution, including the decompositions of
                         its <i>ln(attendance numbers)</i> series.<br>
        :param code: The health board & institution/hospital codes of an institution/hospital.<br>
        :return:
        """

        # Setting data frequency
        training.index.freq = self.__arguments.get('frequency')

        # Modelling
        system: tfc.STLForecastResults = src.modelling.fundamental.Fundamental(
            training=training, arguments=self.__arguments, code=code).exc()

        if system is None:
            system: tfc.STLForecastResults = src.modelling.seasonal.Seasonal(
                training=training, arguments=self.__arguments, code=code).exc()

        return system
