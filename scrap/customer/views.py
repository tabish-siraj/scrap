from django.shortcuts import render
from users.models import User, PersonalDetails
from main.models import Appointment, Material

# Create your views here.

def customer_index(request):
    return render(request, 'customer/index.html')

def customer_edit_profile(request):
    context = {}
    personal_details = PersonalDetails.objects.filter(user=request.user).first()

    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        mobile_number = request.POST['mobile_number']
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        cnic = request.POST['cnic']

        user = User.objects.filter(email=request.user.email).first()
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        if personal_details:
            personal_details.mobile_number = mobile_number
            personal_details.address1 = address1
            personal_details.address2 = address2
            personal_details.city = city
            personal_details.state = state
            personal_details.country = country
            personal_details.cnic = cnic
            personal_details.save()
        else:
            PersonalDetails.objects.create(
                user=user,
                mobile_number=mobile_number,
                address1=address1,
                address2=address2,
                city=city,
                state=state,
                country=country,
                cnic=cnic
            )
        context['success'] = "Profile updated successfully"
    context.update({
        'personal_details': personal_details
    })

    print(context)
        
    return render(request, 'customer/edit_profile.html', context)

def create_appointment(request):
    materials = Material.objects.all()
    context = {}

    context.update({
        'materials': materials
    })
    return render(request, 'customer/create_appointment.html', context)