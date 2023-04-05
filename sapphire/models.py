from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    employeeID = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.otp_code

# class User(AbstractUser):
#     employeeID = models.CharField(max_length=200, blank=True, null=True)
#     email = models.EmailField(max_length=200, unique=True)
#     email_otp = models.CharField(max_length=200, blank=True, null=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

