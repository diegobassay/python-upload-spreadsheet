from django.db import models

class Sales(models.Model):
    purchaser_name = models.CharField(max_length=200)
    item_description = models.CharField(max_length=200)
    item_price = models.FloatField(max_length=200)
    purchase_count = models.IntegerField(default=1)
    merchant_address = models.CharField(max_length=200)
    merchant_name = models.CharField(max_length=200)