from django.shortcuts import get_object_or_404
from fx.models import FxOHLC
import requests
from dotenv import load_dotenv
import os
import json


load_dotenv()

fetch_data = False


def consuming_tiingo_api():
    historical_data = {}
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {os.environ.get('TIINGO_API_TOKEN')}",
    }
    requestResponse = requests.get(
        "https://api.tiingo.com/tiingo/fx/eurusd/prices?startDate=2020-01-01&resampleFreq=1day",
        headers=headers,
    )
    for i in requestResponse.json():
        print(i)
        response_data = FxOHLC(
            date=i["date"],
            ticker=i["ticker"],
            open=i["open"],
            high=i["high"],
            low=i["low"],
            close=i["close"],
        )
        response_data.save()


if fetch_data:
    consuming_tiingo_api()
