from django.urls import path
from django.conf.urls import include, url
from . import views

urlpatterns = [
    path('', views.signupMOH, name='MOH'),
    path('upldcert', views.uploadCovidCert, name='uploadCovidCert'),
    path('search', views.search, name='search'),
    path('home', views.home_MOH, name='home_MOH')
]
