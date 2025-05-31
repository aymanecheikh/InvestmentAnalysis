from django.core.management.base import BaseCommand
from fx.models import CryptoRT
import os
import requests


class Command(BaseCommand):
    help = "Fetches data"

    def handle(self, *args, **options):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {os.environ.get('TIINGO_API_TOKEN')}",
        }
        requestResponse = requests.get(
            "https://api.tiingo.com/tiingo/crypto/prices?tickers=btcusd",
            headers=headers,
        )

        response = requestResponse.json()[0]
        price_data = response["priceData"][-1]

        response_data = CryptoRT(
            ticker=response["ticker"],
            baseCurrency=response["baseCurrency"],
            quoteCurrency=response["quoteCurrency"],
            open=price_data["open"],
            high=price_data["high"],
            low=price_data["low"],
            close=price_data["close"],
            date=price_data["date"],
            tradesDone=price_data["tradesDone"],
            volume=price_data["volume"],
            volumeNotional=price_data["volumeNotional"],
        )
        response_data.save()
