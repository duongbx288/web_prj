from django.db import models
from authentication.models import User

# Create your models here.
class MOH(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    health_authority = models.CharField(max_length=100)
    position = models.CharField(max_length=100)


class CovidCertificate(models.Model):
    national_id = models.CharField(max_length=12, primary_key=True, unique=True, default='')
    fullname = models.CharField(max_length=500, null=True)
    DoB = models.DateField('Date of Birth', blank=True, null=True)
    gender = models.CharField(max_length=10, null=True)
    phone_number = models.CharField(max_length=12, null=True)
    no_of_vaccination = models.SmallIntegerField()
    vaccine_no1_type = models.CharField(max_length=100, null=True)
    vaccination_no1_date = models.DateField(blank=True, null=True)
    vaccine_no2_type = models.CharField(max_length=100, null=True)
    vaccination_no2_date = models.DateField(blank=True, null=True)
