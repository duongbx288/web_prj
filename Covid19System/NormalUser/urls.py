from django.urls import path
from django.conf.urls import include, url
from . import views

urlpatterns = [
    # path('upldprovincels/', views.uploadProvinceCityWardList, name="upload_province_city_ward_list"),
    path('profile/', views.profile, name='profile'),
    path('editprofile/', views.edit_profile, name='edit_profile'),
    path('kbyt/', views.medical_declaration, name='medical_declaration'),
    path('showkbytlist/', views.show_kbyt_list, name='show_kbyt_list'),
    path('showkbytdetail/<int:id>', views.show_kbyt_detail, name='show_kbyt_detail'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('ajax/load-wards/', views.load_wards, name='ajax_load_wards'),
]

