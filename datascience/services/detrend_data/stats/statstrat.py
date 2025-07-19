from abc import ABC, abstractmethod
import warnings

from statsmodels.tsa.stattools import InterpolationWarning, ValueWarning, adfuller, kpss

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


class VarianceReduction(ComparativeStatistic):
    def test_detrend(self, raw_data, detrended_data) -> str:
        return f"{raw_data.Close.var() - detrended_data.dropna().var()}"  # type: ignore

    def __str__(self) -> str:
        return "VarianceReduction"
