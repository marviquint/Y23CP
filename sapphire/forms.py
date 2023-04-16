from django import forms
from django.contrib.auth.forms import PasswordChangeForm


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add a class to each input field
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

class ScrapeForm(forms.Form):
    url = forms.CharField(label='Enter URL to Scrape', max_length=255)

