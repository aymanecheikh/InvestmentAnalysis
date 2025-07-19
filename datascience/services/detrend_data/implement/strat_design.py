from abc import ABC, abstractmethod
from pandas import Series
from scipy.signal import detrend
import numpy as np
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose


class DetrendingStrategy(ABC):
    @abstractmethod
    def detrend(self, data) -> Series:
        pass


class LinearSignalDetrendingStrategy(DetrendingStrategy):
    def detrend(self, data):
        return Series(detrend(data.Close, type="linear"))

    def __str__(self) -> str:
        return "Linear Signal"


class ConstantSignalDetrendingStrategy(DetrendingStrategy):
    def detrend(self, data) -> Series:
        return Series(detrend(data.Close, type="constant"))

    def __str__(self) -> str:
        return "Constant Signal"


class DifferenceDetrendingStrategy(DetrendingStrategy):
    def detrend(self, data):
        return data.Close.diff()

    def __str__(self) -> str:
        return "Difference"


class ReturnsDetrendingStrategy(DetrendingStrategy):
    def detrend(self, data):
        return data.Close.pct_change()

    def __str__(self) -> str:
        return "Returns"


class LogReturnsDetrendingStrategy(DetrendingStrategy):
    def detrend(self, data):
        return np.log(data.Close).diff()

    def __str__(self) -> str:
        return "Log Returns"


class LinearRegressionDetrendingStrategy(DetrendingStrategy):
    def detrend(self, data):
        time = np.arange(len(data.index)).reshape(-1, 1)
        values = data.Close.values.reshape(-1, 1)
        model = LinearRegression().fit(time, values)
        data["Trend"] = model.predict(time)
        result = data.Close - data.Trend
        return result

    def __str__(self) -> str:
        return "Linear Regression"


class SMASmoothingDetrendingStrategy(DetrendingStrategy):
    def detrend(self, data):
        return data.Close - data.Close.rolling(window=12).mean()

    def __str__(self) -> str:
        return "Simple Moving Average Smoothing"


class HoltDetrendingStrategy(DetrendingStrategy):
    def detrend(self, data):
        model = ExponentialSmoothing(data.Close, seasonal=None)
        fit = model.fit()
        data["Trend"] = fit.fittedvalues
        result = data.Close - data.Trend
        return result

    def __str__(self) -> str:
        return "Holt Winters"


class DecompositionDetrendingStrategy(DetrendingStrategy):
    def detrend(self, data):
        decomposition = seasonal_decompose(data.Close, model="additive", period=12)
        data["Trend"] = decomposition.trend
        data["Seasonal"] = decomposition.seasonal
        data["Adjusted"] = data.Close - data.Trend - data.Seasonal
        return data.Adjusted

    def __str__(self) -> str:
        return "Decomposition"
