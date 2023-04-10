from django.shortcuts import render, redirect
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

@login_required
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

@login_required
def home(request):
    if request.user.first_login:
        # if user is logging in for the first time, show the modal
        request.user.first_login = False
        request.user.show_modal = False
        request.user.save()
        return render(request, 'base/home.html', {'show_modal': True})
    else:
        return render(request, 'base/home.html')

@login_required
def search(request):
    return render(request, 'base/searchtool.html')

@login_required
def url(request):
    websites = Website.objects.all()
    return render(request, 'base/url.html', {'websites': websites})

@login_required
def signout(request):
    logout(request)
    return redirect('index')
