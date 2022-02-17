from django.urls import path
from django.conf.urls import include, url
from . import views

urlpatterns = [
    path('add/', views.add, name="add"),
    path('list-moh/', views.listMoh, name="list-moh"),
    path('list-normal/', views.listNormal, name="list-normal"),
    path('update/<id>', views.update, name="update"),
    path('delete/<id>', views.delete, name="delete"),
    path('upload/', views.upload, name="upload"),
    path('login/', views.signin, name="login"),
    path('logout/', views.signout, name="logout"),
]