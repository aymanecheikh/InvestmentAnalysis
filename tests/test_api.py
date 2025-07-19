from fastapi.testclient import TestClient
from datascience.api import app
import pytest
import yfinance as yf

from datascience.services.detrend_data.implement.strat_design import DetrendingStrategy
from datascience.services.detrend_data.stats.statstrat import (
    ComparativeStatistic,
    PureStatistic,
)

client = TestClient(app)


@pytest.fixture(
    params=[
        "1m",
        "2m",
        "5m",
        "15m",
        "30m",
        "60m",
        "90m",
        "1h",
        "1d",
        "5d",
        "1wk",
        "1mo",
        "3mo",
    ]
)
def data_feed(request):
    columns = [
        "Datetime",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Dividends",
        "StockSplits",
    ]

    return (
        yf.Ticker("AAPL")
        .history(period="max", interval=request.param)
        .reset_index()
        .set_axis(columns, axis=1)
        .to_json(orient="records", date_format="iso")
    )


def test_health():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Server is running"


def test_consume_data(data_feed):
    response = client.post(
        url="http://127.0.0.1:8000/test/consume/stockdata", content=data_feed
    )
    assert response.status_code == 200
    assert response.json() == data_feed


def test_implement_detrending_strategy(data_feed):
    response = client.post(
        url="http://127.0.0.1:8000/test/detrend/implement", content=data_feed
    )
    assert response.status_code == 200
    assert len(response.json()) == len(DetrendingStrategy.__subclasses__())


def test_detrending_statistics(data_feed):
    response = client.post(
        url="http://127.0.0.1:8000/test/detrend/stats", content=data_feed
    )
    assert response.status_code == 200
    assert len(response.json()) == len(DetrendingStrategy.__subclasses__())
    for statistic in range(len(DetrendingStrategy.__subclasses__())):
        assert len(response.json()[statistic]) == len(
            PureStatistic.__subclasses__()
        ) + len(ComparativeStatistic.__subclasses__())
