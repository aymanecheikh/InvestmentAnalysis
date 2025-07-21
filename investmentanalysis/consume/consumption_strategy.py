from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from functools import cache
from typing import Any

from pandas import DataFrame, Series
import yfinance as yf


@dataclass(unsafe_hash=True)
class HistoricalData(ABC):
    symbol: str
    start_time: str
    end_time: str
    interval: str

    @abstractmethod
    @cache
    def historical_data(self) -> DataFrame:
        ...

    @property
    def close_data(self) -> Series | Any | DataFrame:
        return self.historical_data()["Close"]
    
    @property
    def get_volume_data(self) -> Series | Any | DataFrame:
        return self.historical_data()["Volume"]


class YahooFinance(HistoricalData):
    @cache
    def historical_data(self) -> DataFrame:
        return yf.Ticker(self.symbol).history(
                start=self.start_time,
                end=self.end_time,
                interval=self.interval
                )


if __name__ == "__main__":
    end_time = datetime.now().date().strftime("%Y-%m-%d")
    yf_hist = YahooFinance(
            symbol="NVDA",
            start_time="2020-01-01",
            end_time=end_time,
            interval="1d"
            )
    print(yf_hist.close_data)
