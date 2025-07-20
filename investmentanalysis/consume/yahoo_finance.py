from dataclasses import dataclass
from datetime import datetime
from pandas import DataFrame
import yfinance as yf


@dataclass
class YahooFinanceHistory:
    symbol: str
    intervals: str
    start_time: datetime
    end_time: datetime

    @property
    def historical_data(self) -> DataFrame:
        return yf.Ticker(self.symbol).history(period="max", intervals=self.intervals)


class CloseData(YahooFinanceHistory):
    def get_close_data(self):
        return self.historical_data["Close"]


class VolumeData(YahooFinanceHistory):
    def get_volume_data(self):
        return self.historical_data["Volume"]
