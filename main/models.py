from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=100)
    product_price = models.FloatField()
    shipping_price = models.FloatField()
    description = models.TextField(max_length=10000)

# Create your models here.
