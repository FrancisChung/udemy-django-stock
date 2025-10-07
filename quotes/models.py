from django.db import models

# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=20)
    date = models.DateField()
    opening_price = models.FloatField()
    closing_price = models.FloatField()

    def __str__(self):
        return self.ticker

