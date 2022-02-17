from django.shortcuts import render, redirect
from django.http import JsonResponse
import pandas as pd


import qrcode
import qrcode.image.svg
from io import BytesIO

from MedicalOfficerOfHealth.models import CovidCertificate
from .forms import MedicalDeclarationForm, NormalUserInfoForm
from .models import MedicalDeclaration, NormalUser, Province, City, Ward
# Create your views here.


def profile(request):
    if request.user.is_authenticated and request.user.is_normal_user is True:
        current_user = request.user

        no_of_vaccination = 0
        try:
            check = CovidCertificate.objects.get(pk=current_user.username)
            no_of_vaccination = check.no_of_vaccination 
        except CovidCertificate.DoesNotExist:
            pass

        try:
            detail_info = NormalUser.objects.get(pk=current_user)
        except:
            normalUser = NormalUser(user=current_user)
            normalUser.save()

        detail_info = NormalUser.objects.get(pk=current_user)

        qr_dict = 'Họ & Tên: ' + current_user.last_name + ' ' + current_user.first_name + '\n' + 'CCCD: ' + current_user.username + '\n' + 'Số mũi vắc xin đã tiêm: ' + str(no_of_vaccination)
        factory = qrcode.image.svg.SvgImage
        img = qrcode.make(qr_dict, image_factory=factory, version=5)
        stream = BytesIO()
        img.save(stream)
        svg = stream.getvalue().decode()
        return render(request, 'profile.html', {'current_user': current_user, 'detail_info': detail_info, 'no_of_vaccination': no_of_vaccination, 'svg': svg})
    elif request.user.is_authenticated and request.user.is_normal_user is False:
        return redirect('home')
    return redirect('login')


def edit_profile(request):
    if request.user.is_authenticated and request.user.is_normal_user is True:
        current_user = request.user

        try:
            person = NormalUser.objects.get(pk=current_user)
        except:
            normalUser = NormalUser(user=current_user)
            normalUser.save()

        person = NormalUser.objects.get(pk=current_user)

        form = NormalUserInfoForm()
        try:
            form = NormalUserInfoForm(instance=person)
        except:
            form =NormalUserInfoForm()
        if request.method == 'POST':
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            current_user.last_name = lname
            current_user.first_name = fname
            current_user.save()
            form = NormalUserInfoForm(request.POST, instance=person)

            if form.is_valid() :
                form.save()
                return redirect('edit_profile')

        return render(request, 'edit_profile.html', {'form': form, 'current_user': current_user})
    elif request.user.is_authenticated and request.user.is_normal_user is False:
        return redirect('home')
    return redirect('login')

def medical_declaration(request):
    if request.user.is_authenticated and request.user.is_normal_user is True:
        current_user = request.user
        form = MedicalDeclarationForm()
        if request.method == 'POST':
            newMedicalDeclaration = MedicalDeclaration(user=current_user)
            # time = newMedicalDeclaration.declarationTime
            newMedicalDeclaration.save()
            # newMedicalDeclaration = MedicalDeclaration.objects.get(user=current_user, declarationTime=time)
            form = MedicalDeclarationForm(request.POST, instance=newMedicalDeclaration)


            if form.is_valid() :
                form.save()
                return redirect('medical_declaration')

        return render(request, 'medical_declaration.html', {'form': form, 'current_user': current_user})
    elif request.user.is_authenticated and request.user.is_normal_user is False:
        return redirect('home')
    return redirect('login')


def show_kbyt_list(request):
    if request.user.is_authenticated and request.user.is_normal_user is True:
        current_user = request.user
        # MedicalDeclaration.objects.filter(full_name="").delete()
        medicalDeclarationList = MedicalDeclaration.objects.filter(user=current_user)
        for medicalDeclaration in medicalDeclarationList:
            print(str(medicalDeclaration.declarationTime))
        ls = {
            "data": medicalDeclarationList
        }
        return render(request, 'medical_declaration_list.html', ls)
    elif request.user.is_authenticated and request.user.is_normal_user is False:
        return redirect('home')
    return redirect('login')


def show_kbyt_detail(request, id):
    if request.user.is_authenticated and request.user.is_normal_user is True:
        current_user = request.user
        print(id)
        medicalDeclaration = MedicalDeclaration.objects.get(pk=id)

        return render(request, 'medical_declaration_detail.html', {'medicalDeclaration': medicalDeclaration})
    elif request.user.is_authenticated and request.user.is_normal_user is False:
        return redirect('home')
    return redirect('login')


# AJAX
def load_cities(request):
    province_id = request.GET.get('province_id')
    cities = City.objects.filter(province_id=province_id).all()
    return render(request, 'city_dropdown_list_options.html', {'cities': cities})

def load_wards(request):
    city_id = request.GET.get('city_id')
    wards = Ward.objects.filter(city_id=city_id).all()
    return render(request, 'ward_dropdown_list_options.html', {'wards': wards})


# def uploadProvinceCityWardList(request):
#     thx_list = pd.read_excel('D:\OneDrive - Hanoi University of Science and Technology\Web technologies and e-Services\web-project\doc\TinhHuyenXa2021.xlsx')
#     province_list = thx_list['Tỉnh Thành Phố'].unique()

#     for index, row in thx_list.iterrows():
#         try:
#             province = Province.objects.get(name=row['Tỉnh Thành Phố'])
#         except:
#             new_entry = Province(name = row['Tỉnh Thành Phố'])
#             new_entry.save()
#             print(row['Tỉnh Thành Phố'])

#         province = Province.objects.get(name=row['Tỉnh Thành Phố'])
#         try:
#             city = City.objects.get(province=province, name=row['Quận Huyện'])
#         except:
#             new_entry = City(province=province, name = row['Quận Huyện'])
#             new_entry.save()

#         city = City.objects.get(province=province, name=row['Quận Huyện'])
#         try:
#             ward = Ward.objects.get(city=city, name = row['Phường Xã'])
#         except:
#             new_entry = Ward(city=city, name = row['Phường Xã'])
#             new_entry.save()

  
#     return redirect('home')
