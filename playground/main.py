from pandas import DataFrame
import yfinance as yf
from numpy import hstack, nan
from numpy.lib.stride_tricks import sliding_window_view


def get_ticker_data(ticker: str) -> DataFrame:
    data: DataFrame
    data = yf.Ticker(ticker).history(period="max", interval="1m").reset_index()
    data["ts_identifier"] = data.apply(
        lambda row: ticker + str(row["Datetime"]), axis=1
    )

    data["accumulation_distribution"] = data.apply(
        lambda row: (row["Close"] - row["Open"])
        / (row["High"] / row["Low"])
        * row["Volume"],
        axis=1,
    )

    data["previous_close"] = data["Close"].shift(1)
    data["true_range"] = data.apply(
        lambda row: max(
            row["High"] - row["Low"],
            row["High"] - row["previous_close"],
            row["previous_close"] - row["Low"],
        ),
        axis=1,
    )
    data["average_true_range"] = data["true_range"].ewm(span=14, adjust=False).mean()

    periods = 14
    aroon_up = 100 * sliding_window_view(data["High"], periods + 1).argmax(1) / periods
    aroon_down = 100 * sliding_window_view(data["Low"], periods + 1).argmin(1) / periods
    data["aroon_up"] = hstack([[nan] * periods, aroon_up])
    data["aroon_down"] = hstack([[nan] * periods, aroon_down])

    return data


def main():
    tickers = [
        "NVDA",
        "AMD",
        "QCOM",
        "AVGO",
        "AMZN",
        "MSFT",
        "GOOGL",
        "INTC",
        "AAPL",
        "IBM",
    ]
    return get_ticker_data(tickers[0])


if __name__ == "__main__":
    print(main())
