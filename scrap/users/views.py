from django.shortcuts import redirect, render
from .models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def register_controller(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, password=password)

        user.save()

        return render(request, 'users/register.html')
    
    return render(request, 'users/register.html')

def login_controller(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
    return render(request, 'users/login.html')

def logout_controller(request):
    logout(request)
    return redirect('/')