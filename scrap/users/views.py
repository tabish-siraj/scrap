from django.shortcuts import redirect, render
from .models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def register_controller(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        user_type = request.POST.get("user_type")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            return render(request, "users/register.html", {"error": "Email already exists"})

        user = User.objects.create_user(
            first_name=firstname, last_name=lastname, email=email, user_type=user_type, password=password
        )
        user.save()
        if user:
            return render(request, "users/register.html", {"success": "Account created successfully. Please login to continue."})
    return render(request, "users/register.html")


def login_controller(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            if user.user_type == "customer":
                return redirect("/customer")
            elif user.user_type == "employee":
                return redirect("/employee")

            return redirect("/")
    return render(request, "users/login.html")


def forgot_password_controller(request):
    return render(request, "users/forgot_password.html")

def logout_controller(request):
    logout(request)
    return redirect("/")
