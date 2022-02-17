from django.http import HttpResponse
from django.shortcuts import redirect, render
from NormalUser.models import MedicalDeclaration
from authentication.models import User

def home(request):
    if request.user.is_authenticated and request.user.is_MOH:
        return redirect('home_MOH')
    return render(request, 'index.html')


def about(request):
    return HttpResponse('about')


def search_F1F2_by_F0id(request):
    if request.method == "POST":
        national_id = request.POST.get('national_id')
        if User.objects.filter(username=national_id):
            pass
        
        if MedicalDeclaration.objects.filter(id_card=national_id):
            pass

    
    return render(request, "search_covid.html")

