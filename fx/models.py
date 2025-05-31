from django.db import models


class FxOHLC(models.Model):
    date = models.DateTimeField()
    ticker = models.CharField(max_length=10)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()


class CryptoRT(models.Model):
    ticker = models.CharField(max_length=10)
    baseCurrency = models.CharField(max_length=10)
    quoteCurrency = models.CharField(max_length=10)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    date = models.DateTimeField()
    tradesDone = models.FloatField()
    volume = models.FloatField()
    volumeNotional = models.FloatField()
