from abc import ABC, abstractmethod
from functools import cache
import warnings
import numpy as np

from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import (
    InterpolationWarning,
    ValueWarning,
    acf,
    pacf,
    adfuller,
    kpss,
)
from statsmodels.tsa.tsatools import detrend

warnings.simplefilter("ignore", InterpolationWarning)
warnings.simplefilter("ignore", ValueWarning)


class PureStatistic(ABC):
    @abstractmethod
    def test_detrend(self, detrended_data) -> str:
        pass


class ComparativeStatistic(ABC):
    @abstractmethod
    def test_detrend(self, raw_data, detrended_data) -> str:
        pass


class ADFullerPValue(PureStatistic):
    def test_detrend(self, detrended_data) -> str:
        return f"{adfuller(detrended_data.dropna())[1]:.4f}"

    def __str__(self) -> str:
        return "ADF"


class KPSSPValue(PureStatistic):
    def test_detrend(self, detrended_data) -> str:
        return f"{kpss(detrended_data.dropna())[1]:.4f}"

    def __str__(self) -> str:
        return "KPSS"


class MeanValue(PureStatistic):
    def test_detrend(self, detrended_data) -> str:
        return detrended_data.dropna().mean()

    def __str__(self) -> str:
        return "Mean"


class AutoCorrelation(PureStatistic):
    def acf_values(self, detrended_data):
        return acf(detrended_data, nlags=30)[1:]
    def pacf_values(self, detrended_data):
        return pacf(detrended_data, nlags=30)[1:]
    def ljungbox_min_pvalue(self, detrended_data):
        return acorr_ljungbox(detrended_data, lags=[10, 20, 30], return_df=True)[
            "lb_pvalue"
        ].min()

    def interpret_values(self, detrended_data):
        return (
            np.mean(np.abs(self.acf_values(detrended_data))),
            np.mean(np.abs(self.pacf_values(detrended_data))),
            np.max(np.abs(self.acf_values(detrended_data))),
            np.max(np.abs(self.pacf_values(detrended_data))),
        )
    
    def _normalize_inverse(self, x, max_acceptable=0.05):
        return min(x / max_acceptable, 1.0)
    def _normalize_pvalue(self, p, threshold=0.05):
        return 1.0 - min(p / threshold, 1.0)
    
    def test_detrend(self, detrended_data) -> str:
        return str(
                sum(
                    self._normalize_inverse(val) * 0.2
                    for val in self.interpret_values(detrended_data)
                    )
                + self._normalize_pvalue(
                    self.ljungbox_min_pvalue(detrended_data)
                    )
                )
    
    def __str__(self) -> str:
        return "AutoCorrelation"


class VarianceReduction(ComparativeStatistic):
    def test_detrend(self, raw_data, detrended_data) -> str:
        return f"{raw_data.Close.var() - detrended_data.dropna().var()}"  # type: ignore

    def __str__(self) -> str:
        return "VarianceReduction"
