from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.signout, name='logout'),
    path('profile/<str:pk>/', views.userProfile, name='userProfile'),
    path('otp/', views.otp, name='otp'),
    path('home/', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('display/', views.display, name='display'),
    path('url/', views.url, name='url'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
