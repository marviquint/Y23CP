from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.signout, name='logout'),
    path('profile/<str:pk>/', views.userProfile, name='userProfile'),
    path('otp/', views.otp, name='otp'),
    path('home/', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('success/', views.success, name='success'),
    path('display/', views.display, name='display'),
    path('url/', views.url, name='url'),
]
