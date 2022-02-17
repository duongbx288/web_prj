from django.contrib.messages import constants
from django.shortcuts import redirect, render

from django.contrib.auth.hashers import check_password
from .models import User
from MedicalOfficerOfHealth.models import CovidCertificate
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from . import utils
from Covid19System import settings
from django.core.mail import send_mail

error_code = {
    1:'Mật khẩu sai. Vui lòng nhập lại mật khẩu',
    2:'Mật khẩu mới không được trùng với mật khẩu cũ',
    3:'Mật khẩu mới và xác nhận mật khẩu không trùng khớp',
    4:'Mật khẩu phải có độ dài tối thiểu 6 ký tự',
}

# Create your views here.
def login_form(request):
    if request.method == "POST":
        if 'sign_up' in request.POST:
            national_id = request.POST.get('national_id')
            email = request.POST.get('email')
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')

            if (len(national_id)==9 or len(national_id)==12) and str(national_id).isdecimal():
                pass
            else:
                messages.error(request, "Số CMT/CCCD không hợp lệ!")
                return render(request, 'login1.html')
            
            if User.objects.filter(username=national_id):
                messages.error(request, "Số CMT/CCCD đã tồn tại!")
                return render(request, 'login1.html')

            if utils.validate_email(email) is False:
                messages.error(request, "Email không hợp lệ!")
                return render(request, 'login1.html')

            if User.objects.filter(email=email):
                messages.error(request, "Email đã tồn tại!")
                return render(request, 'login1.html')

            if pass1 != pass2:
                messages.error(request, "Mật khẩu và mật khẩu xác nhận không khớp!")
                return render(request, 'login1.html')

            myuser = User.objects.create_user(national_id, email, pass2)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()

            messages.success(request, "Tài khoản của bạn đã được tạo thành công")
            return render(request, 'login1.html')

        elif 'sign_in' in request.POST:
            national_id = request.POST['national_id']
            passwd = request.POST['pass']

            user = authenticate(username=national_id, password=passwd)

            if user is not None:
                login(request, user)
                userType = "thang nao day"
                if user.is_normal_user:
                    no_of_vaccination = 0
                    try:
                        check = CovidCertificate.objects.get(pk=user.username)
                        no_of_vaccination = check.no_of_vaccination 
                    except CovidCertificate.DoesNotExist:
                        pass
                    userType = 'Normal User ' + "Da Tiem " + str(no_of_vaccination) + " mui vacxin"
                elif user.is_MOH:
                    userType = 'MOH'
                return render(request, "index.html", {'fname':userType})
            else:
                messages.error(request, "Số CMT/CCCD hoặc mật khẩu của bạn không chính xác!")
                return render(request, 'login2.html')

    return render(request, 'login2.html')


def signout(request):
    logout(request)
    # messages.success(request, "Logged Out Successfully")
    return redirect('home')

def forget_passwd(request):
    if request.method == "POST":
        national_id = request.POST.get('national_id')
        email = request.POST.get('email')
        try:
            user= User.objects.get(username=national_id, email=email)
            new_password = '123456'
            user.set_password(new_password)
            user.save()

            # Send Reset-Password Email
            subject = "Reset Password"
            message = "Dear " + user.first_name + ",\nYour new password is: " + new_password + "\n\n\n\nPlease don't reply this email.\nCOVID Prevention System - http://127.0.0.1:8000/"
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)

            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "Số CMT/CCCD hoặc email của bạn không chính xác!")
            return render(request, 'forget_passwd.html')

    return render(request, 'forget_passwd.html')

@login_required(login_url='/login')
def change_passwd(request):
    if request.method == 'POST':
        current_user = request.user        
        old_pass = request.POST['old_pass']
        new_pass = request.POST['new_pass']
        new_pass2 = request.POST['new_pass2']
        code = validatePasswordChange(current_user, old_pass, new_pass, new_pass2)
        if code==0:
            current_user.set_password(new_pass2)
            current_user.save()
            update_session_auth_hash(request, current_user)  # Important!
            messages.success(request, 'Mật khẩu cập nhật thành công!')
            # Send Reset-Password Email
            subject = "Change Password"
            message = "Dear " + current_user.first_name + ",\nYour new password is: " + new_pass2 + "\n\n\n\nPlease don't reply this email.\nCOVID Prevention System - http://127.0.0.1:8000/"
            from_email = settings.EMAIL_HOST_USER
            to_list = [current_user.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
        else:
            messages.error(request, error_code[code])
            
    return render(request, 'change_passwd.html')
    
def validatePasswordChange(current_user, old_pass, new_pass, new_pass2):
    current_pass = current_user.password
    check_pass = check_password(old_pass, current_pass)
    if not check_pass:
        return 1
    if old_pass == new_pass:
        return 2
    if new_pass != new_pass2:
        return 3
    if len(new_pass2) < 6: 
        return 4 
    return 0