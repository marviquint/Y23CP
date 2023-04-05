from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from sapphire.models import User, OTP
import random
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib import messages


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
            send_mail(
                'Sapphire Login OTP',
                f'Your login OTP is {otp}. Please do not share this with anyone.',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'OTP sent to your email.')
            return redirect('otp')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'base/index.html')

def otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user_otp = OTP.objects.filter(user=request.user, otp_code=otp).first()
        if user_otp:
            # delete OTP from database after successful login
            user_otp.delete()
            messages.success(request, 'You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid OTP.')
    return render(request, 'base/otp.html')

def home(request):
    return render(request, 'base/home.html')

def search(request):
    return render(request, 'base/searchtool.html')

def url(request):
    return render(request, 'base/url.html')

def signout(request):
    logout(request)
    return redirect('index')
