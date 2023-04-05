from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    employeeID = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, unique=True)
    otp = models.CharField(max_length=200, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
