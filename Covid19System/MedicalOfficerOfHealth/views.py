from datetime import date, datetime
from django.contrib.auth import models
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.messages.api import error
from django.contrib.messages.constants import ERROR
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import MOH, CovidCertificate
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import pandas as pd
import os
from authentication.models import User
from django.core.paginator import Paginator
import qrcode
import qrcode.image.svg
from io import BytesIO

# Create your views here.
def MOH_check(user):
    return user.is_MOH

@login_required(login_url='/MOH')
@user_passes_test(MOH_check, login_url='/')
def home_MOH(request):
    current_user = request.user
    qr_dict = 'Họ & Tên: ' + current_user.last_name + ' ' + current_user.first_name + '\n' + 'ID nhân viên: ' + current_user.username
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(qr_dict, image_factory=factory, version=5)
    stream = BytesIO()
    img.save(stream)
    svg = stream.getvalue().decode()
    return render(request, 'home_MOH.html', {'svg': svg})

def signupMOH(request):
    if request.method == "POST":
        national_id = request.POST['national_id']
        passwd = request.POST['pass']

        user = authenticate(username=national_id, password=passwd)

        if user is not None and user.is_MOH:
            login(request, user)
            return redirect('home_MOH')
        else:
            messages.error(request, "ID hoặc mật khẩu của bạn không chính xác!")
            return render(request, 'login_MOH.html')
            
    return render(request, 'login_MOH.html')

@login_required(login_url='/MOH')
@user_passes_test(MOH_check, login_url='/')
def uploadCovidCert(request):
    if request.method == 'POST' and 'vaccine_1st' in request.POST:
        myfile = request.FILES['vaccine_1st']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        covid_certificate = pd.read_excel(str(filename), converters={'national_id': str, 'phone_number': str, 'DoB':str, 'vaccination_date': str})
        for index, row in covid_certificate.iterrows():
            error = 'Hàng ' + str(index+1)
            try:
                body = validateInfo(row)
                if body:
                    error += body
                    raise Exception
                
                old_entry = CovidCertificate.objects.filter(pk=row['national_id'])
                if old_entry:
                    error += " cập nhật thông tin không thành công"
                    old_entry.update(fullname=row['fullname'],
                                    DoB= datetime.strptime(row['DoB'], '%d/%m/%Y').date(),
                                    gender=row['gender'],
                                    phone_number=row['phone_number'],
                                    no_of_vaccination=1,    
                                    vaccine_no1_type=row['vaccine_type'],
                                    vaccination_no1_date=datetime.strptime(row['vaccination_date'], '%d/%m/%Y').date())
                else:
                    error += " thêm thông tin CMTND/CCCD không thành công"
                    new_entry = CovidCertificate(national_id=row['national_id'], 
                                    fullname=row['fullname'],
                                    DoB= datetime.strptime(row['DoB'], '%d/%m/%Y').date(),
                                    gender=row['gender'],
                                    phone_number=row['phone_number'],
                                    no_of_vaccination=1,
                                    vaccine_no1_type=row['vaccine_type'],
                                    vaccination_no1_date=datetime.strptime(row['vaccination_date'], '%d/%m/%Y').date())    
                    new_entry.save()
            except Exception:
                messages.error(request, error)

        os.remove(str(filename))

    elif request.method == 'POST' and 'vaccine_2nd' in request.POST:
        myfile = request.FILES['vaccine_2nd']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        covid_certificate = pd.read_excel(str(filename), converters={'national_id': str, 'phone_number': str, 'DoB': str, 'vaccination_date': str})
        for index, row in covid_certificate.iterrows():
            error = 'Hàng ' + str(index+1)
            try:
                new_entry = CovidCertificate.objects.get(pk=row['national_id'])
                body = validateInfo(row, new_entry)
                if body:
                    error += body
                    raise Exception
                new_entry.phone_number = row['phone_number']
                new_entry.no_of_vaccination = 2
                new_entry.vaccine_no2_type = row['vaccine_type']
                new_entry.vaccination_no2_date = datetime.strptime(row['vaccination_date'], '%d/%m/%Y').date()
                new_entry.save()
            except CovidCertificate.DoesNotExist:
                err_msg = row['fullname'] + ' với số CMT/CCCD: ' + row['national_id'] + ' chưa có dữ liệu tiêm mũi 1 trong hệ thống!'
                messages.error(request, err_msg)

        os.remove(str(filename))
        
    return render(request, 'upload_covid_cert.html')

def validateInfo(row, new_entry=None):
    id = row['national_id']
    fullname = str(row['fullname']).replace(" ","")
    phone = row['phone_number']
    if (len(id)!=9 and len(id)!=12) or not str(id).isdigit():
        error = " số CMND/CCCD không hợp lệ"
    elif not fullname.isalpha():
        error = " họ tên không hợp lệ"
    elif len(phone)!=10 or not str(phone).isdigit():
        error = " số điện thoại không hợp lệ"
    elif new_entry and new_entry.vaccination_no1_date > datetime.strptime(row['vaccination_date'], '%d/%m/%Y').date():
        error = " ngày tiêm mũi 2 không hợp lệ"
    else:
        return None
    return error
    
@login_required(login_url='/MOH')
@user_passes_test(MOH_check, login_url='/')
def search(request):
    if not request.method=='POST':
        records = CovidCertificate.objects.all()
        target = ''
    else:
        target = request.POST['target']
        records = CovidCertificate.objects.filter(pk=target) | CovidCertificate.objects.filter(fullname=target)
    
    paginator = Paginator(records, 25) # Show 25 records per page.

    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'search_MOH.html', {'page':page_obj, 'target':target})