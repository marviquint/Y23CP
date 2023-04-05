from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.site_header = "Sapphire Administrator"
admin.site.site_title = "Sapphire Admin Area"
admin.site.index_title = "Sapphire Admin"

class Admin(UserAdmin):
    list_display = ['employeeID', 'firstName', 'lastName' , 'email', 'password', 'otp']


admin.site.register(User, UserAdmin)