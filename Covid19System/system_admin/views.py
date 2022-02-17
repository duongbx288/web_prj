from datetime import date, datetime
from django.contrib import auth
from django.contrib.auth import login, models
from django.contrib.messages.api import error
from django.contrib.messages.constants import ERROR
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
import pandas as pd
import os
from authentication.models import User
from . import utils
from django.core.paginator import Paginator
# Create your views here.


def add(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            national_id = request.POST.get('national_id')
            email = request.POST.get('email')
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')

            if (len(national_id) == 9 or len(national_id) == 12) and str(national_id).isdecimal():
                pass
            else:
                messages.error(request, "Số CMT/CCCD không hợp lệ!")
                return render(request, 'add_user.html')

            if User.objects.filter(username=national_id):
                messages.error(request, "Số CMT/CCCD đã tồn tại!")
                return render(request, 'add_user.html')

            if utils.validate_email(email) is False:
                messages.error(request, "Email không hợp lệ!")
                return render(request, 'add_user.html')

            if User.objects.filter(email=email):
                messages.error(request, "Email đã tồn tại!")
                return render(request, 'add_user.html')

            if pass1 != pass2:
                messages.error(
                    request, "Mật khẩu và mật khẩu xác nhận không khớp!")
                return render(request, 'add_user.html')

            myuser = User.objects.create_user(national_id, email, pass2)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.is_MOH = True
            myuser.is_normal_user = False
            myuser.save()

            messages.success(request, "Tài khoản của bạn đã được tạo thành công")
            return render(request, 'add_user.html')

        return render(request, 'add_user.html')
    else:
        messages.success(request, "Vui lòng đăng nhập để tiếp tục")
        return redirect('http://127.0.0.1:8000/sys_admin/login')

def listMoh(request):
    if request.user.is_authenticated:
        list = User.objects.filter(is_MOH = True)
        paginator = Paginator(list, 10) # Show 25 records per page.
        page_number = request.GET.get('page',1)
        page_obj = paginator.get_page(page_number)
        list = {
            'page': page_obj,
            'role' : 'nhân viên y tế',
        }
        return render(request, 'list_user.html', list)
    else:
        messages.error(request, "Vui lòng đăng nhập để tiếp tục")
        return redirect('http://127.0.0.1:8000/sys_admin/login')

def listNormal(request):
    if request.user.is_authenticated:
        list = User.objects.filter(is_normal_user = True)
        paginator = Paginator(list, 10) # Show 25 records per page.
        page_number = request.GET.get('page',1)
        page_obj = paginator.get_page(page_number)
        list = {
            'page': page_obj,
            'role' : 'Người dùng thường',
        }
        return render(request, 'list_user.html', list)
    else:
        messages.error(request, "Vui lòng đăng nhập để tiếp tục")
        return redirect('http://127.0.0.1:8000/sys_admin/login')

def update(request, id):
    if request.user.is_authenticated:
        user1 = {
            'user': User.objects.get(id=id)
        }
        if request.method == 'POST':
            national_id = request.POST.get('national_id')
            email = request.POST.get('email')
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            user = User.objects.get(id=id)
            if (len(national_id) == 9 or len(national_id) == 12) and str(national_id).isdecimal():
                pass
            else:
                messages.error(request, "Số CMT/CCCD không hợp lệ!")
                return render(request, 'update_user.html', user1)

            if User.objects.filter(username=national_id) and national_id != User.objects.get(id=id).username:
                messages.error(request, "Số CMT/CCCD đã tồn tại!")
                return render(request, 'update_user.html', user1)

            if utils.validate_email(email) is False:
                messages.error(request, "Email không hợp lệ!")
                return render(request, 'update_user.html', user1)

            if User.objects.filter(email=email) and email != User.objects.get(id=id).email:
                messages.error(request, "Email đã tồn tại!")
                return render(request, 'update_user.html', user1)
            user.username = national_id
            user.email = email
            user.first_name = fname
            user.last_name = lname
            user.save()
            user_ = {
                'user': User.objects.get(id=id)
            }
            messages.success(request, "Cập nhật tài khoản thành công")
            return render(request, 'update_user.html', user_)
    else:
        messages.error(request, "Vui lòng đăng nhập để tiếp tục")
        return redirect('http://127.0.0.1:8000/sys_admin/login')
    
    return render(request, 'update_user.html', user1)

def delete(request, id):
    if request.user.is_authenticated:
        user = User.objects.get(id=id)
        user.delete()
        messages.success(request, "Tài khoản của bạn đã xóa thành công")
        return redirect("http://127.0.0.1:8000/sys_admin/list")
    else:
        messages.error(request, "Vui lòng đăng nhập để tiếp tục")
        return redirect('http://127.0.0.1:8000/sys_admin/login')

def upload(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            regist_sucess = 0
            myfile = request.FILES['file_user']
            fs = FileSystemStorage()
            file_user = fs.save(myfile.name, myfile)
            list_user = pd.read_excel(str(file_user), converters={
                                    'national_id': str, 'email': str, 'first_name': str, 'last_name': str})
            for index, row in list_user.iterrows():
                print(row['national_id']+row['email']+row['first_name']+row['last_name'])
                if (len(row['national_id']) == 9 or len(row['national_id']) == 12) and str(row['national_id']).isdecimal():
                    pass
                if User.objects.filter(username=row['national_id']) or utils.validate_email(row['email']) is False or User.objects.filter(email=row['email']) :
                    pass
                else:
                    user = User.objects.create_user(row['national_id'], row['email'],row['national_id'])
                    user.first_name = row['first_name']
                    user.last_name = row['last_name']
                    user.is_MOH = True
                    user.is_normal_user = False
                    user.save()
                    regist_sucess = regist_sucess + 1
            convert_string = str(regist_sucess)     
            messages.success(request, convert_string + "tài khoản đã được tạo thành công")
            return render(request, 'upload.html')    
    else:
        messages.error(request, "Vui lòng đăng nhập để tiếp tục")
        return redirect('http://127.0.0.1:8000/sys_admin/login')
    return render(request, 'upload.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        authen = authenticate(username=username,password=password,is_superuser=True)
        if authen is None:
            messages.success(request, "Tài khoản của bạn không đúng")
            return redirect("http://127.0.0.1:8000/sys_admin/login")
        login(request,authen)
        return redirect("http://127.0.0.1:8000/sys_admin/list-moh")
    return render(request, 'login.html')

def signout(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/sys_admin/login')
