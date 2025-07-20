from dataclasses import dataclass
from datetime import datetime
from binance.client import Client
import os
import pandas as pd

api_key = os.environ.get("BINANCE_API_KEY")
api_secret = os.environ.get("BINANCE_API_SECRET")

client = Client(api_key, api_secret)


@dataclass
class BinanceHistory:
    symbol: str
    start_time: str
    end_time: str
    interval: str

    @property
    def historical_data(self):
        klines = client.get_historical_klines(
            symbol=self.symbol,
            interval=Client.KLINE_INTERVAL_1MINUTE,
            start_str=self.start_time,
            end_str=self.end_time,
        )
        df_M = pd.DataFrame(
            klines,
            columns=[
                "Open Time",
                "Open",
                "High",
                "Low",
                "Close",
                "Volume",
                "Close Time",
                "Quote Asset Volume",
                "Number of Trades",
                "Taker Buy Base Asset Volume",
                "Taker Buy Quote Asset Volume",
                "Ignore",
            ],
        )
        columns_to_convert = [
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "Quote Asset Volume",
            "Number of Trades",
            "Taker Buy Base Asset Volume",
            "Taker Buy Quote Asset Volume",
        ]

        for col in columns_to_convert:
            df_M[col] = df_M[col].astype(float)

        return df_M


class CloseData(BinanceHistory):
    def get_close_data(self):
        return self.historical_data["Close"]

class VolumeData(BinanceHistory):
    def get_volume_data(self):
        return self.historical_data["Volume"]
