from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from sapphire.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
    
        try:
            user = User.objects.get(email=email)
        except:
            return render(request, 'base/index.html', {'error': 'User Does Not Exists!'})
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'base/index.html', {'error': 'Invalid Credentials!'})
    
    return render(request, 'base/index.html')

def otp(request):
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
