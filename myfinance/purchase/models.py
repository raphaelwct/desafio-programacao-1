from django.db import models


class Purchase(models.Model):
    purchaser = models.ForeignKey('Purchaser')
    item = models.ForeignKey('Item')
    merchant = models.ForeignKey('Merchant')
    count = models.IntegerField()


class Purchaser(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Item(models.Model):
    description = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=18, decimal_places=2)


class Merchant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=255)
