from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    """Our custom user model that adds a new field to the default django user model"""
    is_employee = models.BooleanField(default=False)
    zipcode = models.CharField(max_length=50, default=None, null=True)
    "we want to add new keys to this object dictionary like you added is_employee"
    "example of our attempt below.."

    def __str__(self):
        return self.username
