from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from sapphire.models import User, OTP, Website
import random
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
from .forms import CustomPasswordChangeForm, ScrapeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from scrapy_project.scrapyproject.scrapyproject.spiders.scrapyspider import QuotesSpider
from scrapy.crawler import CrawlerProcess, CrawlerRunner
import os, sys
from django.conf import settings
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
import json
from scrapy import signals
from django.contrib import messages
from twisted.internet import reactor
from scrapy.signalmanager import dispatcher
from django.dispatch import receiver
from django.core.signals import request_finished


# Create your views here.

def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # generate OTP
            otp = get_random_string(length=6, allowed_chars='0123456789')
            # save OTP to database
            OTP.objects.create(user=user, otp_code=otp)
            # send OTP to user's email
            subject = 'Your OTP for Sapphire Login'
        
            message = f'Hello {user.first_name},<br><br>Your login OTP is <b>{otp}</b>. Please do not share this with anyone.<br><br>Best Regards,<br><br><b>Sapphire Admin</b>'
            recipient_list = [user.email]
            from_email = settings.DEFAULT_FROM_EMAIL
            send_mail(subject, strip_tags(message), from_email, recipient_list, html_message=message, fail_silently=False)
            return redirect('otp')
        else:
            return render(request,'base/index.html', {'error': 'Invalid credentials'})
    return render(request, 'base/index.html')

# @login_required
def otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user_otp = OTP.objects.filter(user=request.user, otp_code=otp).first()
        if user_otp:
            # delete OTP from database after successful login
            user_otp.delete()
            return redirect('home')
        else:
            return render(request,'base/otp.html', {'error': 'Invalid OTP!'})
    return render(request, 'base/otp.html')

# @login_required
def home(request):
    if request.user.first_login:
        # if user is logging in for the first time, show the modal
        request.user.first_login = False
        request.user.show_modal = False
        request.user.save()
        return render(request, 'base/home.html', {'show_modal': True})
    else:
        return render(request, 'base/home.html')

# @login_required
class DjangoScrapyMiddleware:
    def __init__(self, get_response=None, crawler_process=None):
        self.get_response = get_response
        self.scraped_data = []
        self.crawler_process = crawler_process
        
    def __call__(self, request):
        if request.method == 'POST':
            url = request.POST.get('url', '')
            if url:
                self.scraped_data = []
                spider = QuotesSpider(search_term=url, scraped_data=self.scraped_data)
                self.crawler_process.crawl(spider.__class__)
                self.crawler_process.start()
                request.session['scraped_data'] = self.scraped_data  # store data in session
                messages.success(request, 'Scraping completed successfully.')
                return redirect('success')
            else:
                messages.error(request, 'Please enter a URL.')
                return redirect('search')
        return self.get_response(request)


def search(request):
    form = ScrapeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        settings = get_project_settings()
        crawler_process = CrawlerProcess(settings)
        print(settings)  # add this line
        middleware = DjangoScrapyMiddleware(get_response=None, crawler_process=crawler_process)
        response = middleware(request)
        return response
    return render(request, 'base/searchtool.html', {'form': form})

def success(request):
    data = request.session.get('scraped_data', []) # retrieve data from session
    return render(request, 'base/success.html', {'data': data})

# @login_required
def url(request):
    websites = Website.objects.all()
    return render(request, 'base/url.html', {'websites': websites})

@login_required
def signout(request):
    logout(request)
    return redirect('index')


@login_required
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    loggedUser = request.user

    # Handle password change form submission
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=loggedUser, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('userProfile', pk=pk)
    else:
        form = CustomPasswordChangeForm(user=user)

    return render(request, 'base/profile.html', {'user': user, 'form': form})
    
