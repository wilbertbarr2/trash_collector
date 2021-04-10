from django.db import models
# Create your models here.

# TODO: Finish customer model by adding necessary properties to fulfill user stories


class Customer(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey('accounts.User', default=None, on_delete=models.CASCADE)
    zipcode = models.CharField(max_length=50, default=None)
    address = models.CharField(max_length=50, default=None)
    state = models.CharField(max_length=50, default=None)
    city = models.CharField(max_length=50, default=None)
    pickup_day = models.CharField(max_length=50, default=None)
    balance = models.IntegerField(default=0)
    onetime_pickup = models.DateField(null=True)
    tem_suspend_start = models.DateField(null=True)
    tem_suspend_end = models.DateField(null=True)
    has_used_one_time_extra_service = models.BooleanField(default=False)
