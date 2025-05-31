from django.core.management.base import BaseCommand
from fx.models import FxOHLC
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
