from django import forms
from django.forms import widgets
from authentication.models import User
from .models import MedicalDeclaration, NormalUser, City, Ward


class DateInput(forms.DateInput):
    input_type = 'date'

class NormalUserInfoForm(forms.ModelForm):
    class Meta:
        model = NormalUser
        # fields = '__all__'
        fields = ('DoB','gender','phone_number', 'province', 'city', 'ward', 'detailed_address')
        widgets = {
            'DoB': DateInput()
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()
        self.fields['ward'].queryset = Ward.objects.none()

        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['city'].queryset = City.objects.filter(province_id=province_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.province.city_set.order_by('name')

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['ward'].queryset = Ward.objects.filter(city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['ward'].queryset = self.instance.city.ward_set.order_by('name')

class NormalUserInfoForm(forms.ModelForm):
    class Meta:
        model = NormalUser
        # fields = '__all__'
        fields = ('DoB','gender','phone_number', 'province', 'city', 'ward', 'detailed_address')
        widgets = {
            'DoB': DateInput()
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()
        self.fields['ward'].queryset = Ward.objects.none()

        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['city'].queryset = City.objects.filter(province_id=province_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.province.city_set.order_by('name')

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['ward'].queryset = Ward.objects.filter(city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['ward'].queryset = self.instance.city.ward_set.order_by('name')


class MedicalDeclarationForm(forms.ModelForm):
    class Meta:
        model = MedicalDeclaration
        fields = ('registerForOtherPeople','full_name','id_card','year_of_birth','gender','nationality',
                 'province', 'city', 'ward', 'detailed_address', 'phone_number', 'email',
                 'past_14d_travel','arrival_province','arrival_city','arrival_ward','arrival_detailed_place',
                 'past_14d_symptoms','deltaild_description','in_contact_confirmed_COVID19_case',
                 'in_contact_people_from_countries_with_COVID19','in_contact_people_with_syptoms')
        widgets = {
            'gender': forms.Select(attrs={'class' : 'select'}),
            'province': forms.Select(attrs={'class' : 'select'}),
            'city': forms.Select(attrs={'class' : 'select'}),
            'ward': forms.Select(attrs={'class' : 'select'}),
            'past_14d_travel': forms.RadioSelect(attrs={'id' : 'arr_addr'}),
            'arrival_province': forms.Select(attrs={'class' : 'select arrival'}),
            'arrival_city': forms.Select(attrs={'class' : 'select arrival'}),
            'arrival_ward': forms.Select(attrs={'class' : 'select arrival'}),
            'arrival_detailed_place': forms.TextInput(attrs={'class' : 'arrival'}),
            'past_14d_symptoms': forms.RadioSelect(attrs={'id' : 'symptoms_deltail'}),
            'in_contact_confirmed_COVID19_case': forms.RadioSelect(),
            'in_contact_people_from_countries_with_COVID19': forms.RadioSelect(),
            'in_contact_people_with_syptoms': forms.RadioSelect()
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()
        self.fields['ward'].queryset = Ward.objects.none()
        self.fields['arrival_city'].queryset = City.objects.none()
        self.fields['arrival_ward'].queryset = Ward.objects.none()

        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['city'].queryset = City.objects.filter(province_id=province_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.province.city_set.order_by('name')

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['ward'].queryset = Ward.objects.filter(city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['ward'].queryset = self.instance.city.ward_set.order_by('name')


        if 'arrival_province' in self.data:
            try:
                province_id = int(self.data.get('arrival_province'))
                self.fields['arrival_city'].queryset = City.objects.filter(province_id=province_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['arrival_city'].queryset = self.instance.province.city_set.order_by('name')

        if 'arrival_city' in self.data:
            try:
                city_id = int(self.data.get('arrival_city'))
                self.fields['arrival_ward'].queryset = Ward.objects.filter(city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['arrival_ward'].queryset = self.instance.city.ward_set.order_by('name')