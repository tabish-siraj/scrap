from django.shortcuts import render
from users import views as users
from main.models import ContactUs
# Create your views here.

def index(request):    
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        city = request.POST.get("city")
        contact = request.POST.get("contact")
        message = request.POST.get("message")

        contact_us = ContactUs.objects.create(name=name, email=email, city=city, contact=contact, message=message)

        return render(request, 'main/index.html', {'success': 'Thank you for your feedback! We will get back to you soon.'})

    return render(request, 'main/index.html')