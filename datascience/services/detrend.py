from abc import ABC, abstractmethod
from pandas import Series
from scipy.signal import detrend
import numpy as np
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import InterpolationWarning, ValueWarning, \
    adfuller, kpss, acf, pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
import warnings

from datascience.services.consume import consume_data


warnings.simplefilter("ignore", InterpolationWarning)
warnings.simplefilter("ignore", ValueWarning)


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
        return data.Close - data.Trend

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
        return data.Close - data.Trend

    def __str__(self) -> str:
        return "Holt Winters"


class DecompositionDetrendingStrategy(DetrendingStrategy):

    def detrend(self, data):
        decomposition = seasonal_decompose(
            data.Close,
            model="additive",
            period=12
        )
        data["Trend"] = decomposition.trend
        data["Seasonal"] = decomposition.seasonal
        data["Adjusted"] = data.Close - data.Trend - data.Seasonal
        return data.Adjusted

    def __str__(self) -> str:
        return "Decomposition"


class DetrendingEvaluator:
        
    def evaluate_autocorrelation(
        self,
        acf_maac,
        ma_pacf,
        max_acf,
        max_pacf,
        ljungbox_min_pvalue
    ):
        def normalize_inverse(x, max_acceptable=0.05):
            return min(x / max_acceptable, 1.0)

        def normalize_pvalue(p, threshold=0.05):
            return 1.0 - min(p / threshold, 1.0)

        score = (
            normalize_inverse(acf_maac) * 0.2 +
            normalize_inverse(ma_pacf) * 0.2 +
            normalize_inverse(max_acf) * 0.2 +
            normalize_inverse(max_pacf) * 0.2 +
            normalize_pvalue(ljungbox_min_pvalue) * 0.2
        )

        return score

    def get_detrending_strategies(self, data):

        raw_data = consume_data(data)
        evaluation = []

        for strategy in DetrendingStrategy.__subclasses__():

            detrended_data = strategy().detrend(raw_data).dropna()

            acf_values = acf(detrended_data, nlags=30)[1:]
            pacf_values = pacf(detrended_data, nlags=30)[1:]
            acf_maac = np.mean(np.abs(acf_values))
            ma_pacf = np.mean(np.abs(pacf_values))
            max_acf = np.max(np.abs(acf_values))
            max_pacf = np.max(np.abs(pacf_values))
            ljungbox_min_pvalue = acorr_ljungbox(
                detrended_data, lags=[10, 20, 30], return_df=True
            )["lb_pvalue"].min()


            strategy_evaluation = {
                str(strategy()): {
                    "ADF": f"{adfuller(detrended_data)[1]:.4f}",
                    "KPSS": f"{kpss(detrended_data)[1]:.4f}",
                    "Mean": f"{detrended_data.mean()}",
                    "Variance Reduction": f"{
                        raw_data.Close.var() - detrended_data.var()
                    }",
                    "Autocorrelation": self.evaluate_autocorrelation(
                        acf_maac,
                        ma_pacf,
                        max_acf,
                        max_pacf,
                        ljungbox_min_pvalue
                    )
                }
            }
            evaluation.append(strategy_evaluation)
        return evaluation

    """
        print("Skewness: TBC")
        print("Kurtosis: TBC")
        print("FFT: TBC")
        print("Rolling mean stability: TBC")
        print("std stability: TBC")
    """


