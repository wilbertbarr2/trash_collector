from django.db import models
# Create your models here.

# TODO: Finish customer model by adding necessary properties to fulfill user stories


class Customer(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey('accounts.User', default=None, on_delete=models.CASCADE)
    zipcode = models.CharField(max_length=50, default=None)
    address = models.CharField(max_length=11, default=None)
    state = models.CharField(max_length=50, default=None)
    city = models.CharField(max_length=50, default=None)
    pickup_day = models.CharField(max_length=50, default=None)
    balance = models.IntegerField(default=None)
    onetime_pickup = models.CharField(max_length=25, default=None)
    tem_suspend_start = models.CharField(max_length=50, default=None)
    tem_suspend_end = models.CharField(max_length=50, default=None)
