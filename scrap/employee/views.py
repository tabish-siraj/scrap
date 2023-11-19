from django.shortcuts import render

# Create your views here.
def employee_index(request):
    return render(request, 'employee/index.html')