from django.shortcuts import render
from users import views as users
# Create your views here.

def index(request):    
    if request.method == "POST" and 'contactus' in request.POST:
        return render(request, 'main/contactus.html')

    return render(request, 'main/index.html')