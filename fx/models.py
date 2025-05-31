from django.db import models


class FxOHLC(models.Model):
    date = models.DateTimeField()
    ticker = models.CharField(max_length=10)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
