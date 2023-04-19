from django import forms
from django.contrib.auth.forms import PasswordChangeForm


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add a class to each input field
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

class ScrapeForm(forms.Form):
    main_url = forms.CharField(
        label='Enter Normal Website URL to Crawl',
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control text-large'})
    )

class PDFScrapeForm(forms.Form):
    pdf_spider_url = forms.CharField(
        label='Enter PDF Website URL to Crawl',
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control text-large'})
    )