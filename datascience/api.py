from pydantic import BaseModel
from datetime import datetime
from fastapi import FastAPI
from typing import List

from datascience.services.detrend_data.strat_facade import DetrendingFacade

from .services.consume import Consumption


class StockData(BaseModel):
    Datetime: datetime
    Open: float
    High: float
    Low: float
    Close: float
    Volume: int
    Dividends: float
    StockSplits: float


app = FastAPI()
data = Consumption()
detrend = DetrendingFacade()


@app.get("/")
def health():
    return "Server is running"


@app.post("/test/consume/stockdata")
def consume(stockdata: List[StockData]):
    return data.consume_data(stockdata).to_json(orient="records", date_format="iso")


@app.post("/test/detrend/implement")
def consume_detrending_strategies(stockdata: List[StockData]):
    return [
        strategy.to_json(orient="records", date_format="iso")
        for strategy in detrend.detrend_data(stockdata)
    ]

@app.post("/test/detrend/stats")
def analyze_detrending_strategies(stockdata: List[StockData]):
    return detrend.run_stats(stockdata)
