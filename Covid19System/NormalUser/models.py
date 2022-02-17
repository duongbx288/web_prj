from django.db import models
from authentication.models import User
from django.utils import timezone

# Create your models here.
class Province(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Ward(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class NormalUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    DoB = models.DateField('Date of Birth', blank=True, null=True)

    GENDER_CHOICE = (
        ('M', 'Nam'),
        ('F', 'Nữ'),
        ('O', 'Khác')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE) # 3 values: M - male, F -female, O - others
    phone_number = models.CharField(max_length=10)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, blank=True, null=True)
    detailed_address = models.CharField(max_length=500)


class MedicalDeclaration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    declarationTime = models.DateTimeField(default=timezone.now, blank=False, null=False)

    registerForOtherPeople = models.BooleanField(default=False)
    full_name = models.CharField(max_length=50)
    id_card = models.CharField(max_length=12)
    year_of_birth = models.CharField(max_length=20)
    GENDER_CHOICE = (
        ('Nam', 'Nam'),
        ('Nữ', 'Nữ'),
        ('Khác', 'Khác')
    )
    gender = models.CharField(max_length=4, choices=GENDER_CHOICE)
    nationality = models.CharField(max_length=20)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, blank=True, null=True)
    detailed_address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    BOOLEAN_CHOICE = (
        ('Không', 'Không'),
        ('Có', 'Có')
    )
    past_14d_travel = models.CharField(max_length=6, choices=BOOLEAN_CHOICE, default=BOOLEAN_CHOICE[0][0])
    arrival_province = models.ForeignKey(Province, related_name='arrival_province', on_delete=models.SET_NULL, blank=True, null=True)
    arrival_city = models.ForeignKey(City, related_name='arrival_city', on_delete=models.SET_NULL, blank=True, null=True)
    arrival_ward = models.ForeignKey(Ward, related_name='arrival_ward', on_delete=models.SET_NULL, blank=True, null=True)
    arrival_detailed_place = models.CharField(max_length=500, blank=True, null=True)

    past_14d_symptoms = models.CharField(max_length=6, choices=BOOLEAN_CHOICE, default=BOOLEAN_CHOICE[0][0])
    deltaild_description = models.CharField(max_length=5000, blank=True, null=True)

    in_contact_confirmed_COVID19_case = models.CharField(max_length=6, choices=BOOLEAN_CHOICE, default=BOOLEAN_CHOICE[0][0])
    in_contact_people_from_countries_with_COVID19 = models.CharField(max_length=6, choices=BOOLEAN_CHOICE, default=BOOLEAN_CHOICE[0][0])
    in_contact_people_with_syptoms = models.CharField(max_length=6, choices=BOOLEAN_CHOICE, default=BOOLEAN_CHOICE[0][0])