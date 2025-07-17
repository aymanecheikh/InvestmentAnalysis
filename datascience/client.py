import requests
import yfinance as yf
import time


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

    def get_detrend_evaluation(self, ticker: str):
        return requests.post(
            "http://127.0.0.1:8000/api/v0/evaluate/detrend/",
            self.get_historical_stock_prices(ticker),
        )

    def get_price_predictions(self, ticker: str):
        return requests.post(
            "http://127.0.0.1:8000/api/v0/predict/prices/",
            self.get_historical_stock_prices(ticker),
        )


start = time.perf_counter()

client = Client()

client.get_detrend_evaluation("NVDA").json()
# client.get_price_predictions("NVDA").json()

end = time.perf_counter()

print(f"Elapsed time: {end - start:.2f} seconds")
