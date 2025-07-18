import requests
import yfinance as yf


class Client:
    def get_historical_stock_prices(self, ticker: str):
        return (
            yf.Ticker(ticker)
            .history(period="max", interval="1m")
            .reset_index()
            .set_axis(
                [
                    "Datetime",
                    "Open",
                    "High",
                    "Low",
                    "Close",
                    "Volume",
                    "Dividends",
                    "StockSplits",
                ],
                axis=1,
            )
            .to_json(orient="records", date_format="iso")
        )

    def get_datafeed(self, ticker: str):
        response = requests.post(
            "http://127.0.0.1:8000/test/datafeed",
            self.get_historical_stock_prices(ticker),
        )
        return response
