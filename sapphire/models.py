from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    employeeID = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, unique=True)
    show_modal = models.BooleanField(default=True)
    first_login = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.first_login = True
        super().save(*args, **kwargs)


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.otp_code

class Website(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=1000)

    def __str__(self):
        return self.name
    

