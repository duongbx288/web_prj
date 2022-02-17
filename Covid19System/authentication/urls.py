from django.urls import path
from django.conf.urls import include, url
from . import views

urlpatterns = [
    path('login', views.login_form, name="login"),
    path('login/forgot', views.forget_passwd, name="forget_passwd"),
    path('signout', views.signout, name="signout"),
    path('change', views.change_passwd, name="change_passwd")

]