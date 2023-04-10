from django.contrib import admin, messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from django.urls import path, reverse

from django import forms

import csv
from django.http import HttpResponseRedirect

from sapphire.signals import user_added
from .models import User as SapphireUser
from .models import Website


admin.site.site_header = "Sapphire Administrator"
admin.site.site_title = "Sapphire Admin Area"
admin.site.index_title = "Sapphire Admin"


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm

    list_display = ['employeeID', 'first_name', 'last_name', 'email']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('employeeID', 'email', 'first_name', 'last_name')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('employeeID', 'first_name', 'last_name','username', 'email', 'password1', 'password2'),
        }),
    )

    def save_model(self, request, obj, form, change):
        # Call the original save_model method to create the user
        super().save_model(request, obj, form, change)

        # Emit the user_added signal with the new user instance
        user_added.send(sender=self.__class__, instance=obj)

class URLCSVImportForm(forms.Form):
    urlcsv_upload = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'file-upload form-control'}))


class WebsiteAdmin(admin.ModelAdmin):
    list_display = ("name", 'url')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('url-upload/', self.upload_url),]
        return new_urls + urls
    

    def upload_url(self, request):
        if request.method == "POST":
            csv_file = request.FILES["urlcsv_upload"]

            if not csv_file.name.endswith(".csv"):
                messages.warning(request, 'Invalid File Type! Must be .csv')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("UTF-8")
            csv_data = file_data.split("\n")
            if not csv_data[-1]:  # Check if the last element is an empty string
                csv_data.pop()  # Remove it from the list
            for x in csv_data:
                fields = x.split(",")
                created = Website.objects.update_or_create(
                    name= fields[0],
                    url = fields[1],
                )
            to = reverse('admin:index')
            return HttpResponseRedirect(to)

        form = URLCSVImportForm()
        data = {"form": form}
        return render(request, "admin/url_upload.html", data)


#admin.site.unregister(User)
admin.site.register(SapphireUser, UserAdmin)
admin.site.register(Website, WebsiteAdmin)

