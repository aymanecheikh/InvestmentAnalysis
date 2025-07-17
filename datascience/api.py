from pydantic import BaseModel
from datetime import datetime
from fastapi import FastAPI
from typing import List

from datascience.services.detrender.detrend import evaluate_detrending_strategies
from .services.predictions import predict_prices


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


@app.get("/")
def read_root():
    return "Server is running"


@app.post("/api/v0/evaluate/detrend")
def evaluate_detrended_prices(stockdata: List[StockData]):
    return evaluate_detrending_strategies(stockdata)


@app.post("/api/v0/predict/prices")
def get_stockdata(stockdata: List[StockData]):
    return predict_prices(stockdata)
