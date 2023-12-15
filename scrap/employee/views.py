from django.shortcuts import render
from main.models import Order, Appointment, Payment, Material, AppointmentStatus
from users.models import User, PersonalDetails, VehicleType
from django.db.models import Sum

# Create your views here.
def employee_index(request):
    return render(request, 'employee/index.html')

def employee_edit_profile(request):
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
        vehicle_no = request.POST['vehicle_no']
        vehicle_type = request.POST['vehicle_type']
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
            personal_details.vehicle_no = vehicle_no
            personal_details.vehicle_type = vehicle_type
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
                vehicle_no=vehicle_no,
                vehicle_type=vehicle_type,
                cnic=cnic
            )
        context['success'] = "Profile updated successfully"
    context.update({
        'personal_details': personal_details,
        'vehicle_types': [vehicle_type.value for vehicle_type in VehicleType],
    })

    return render(request, 'employee/edit_profile.html', context)

def employee_appointments(request):
    appointments = Appointment.objects.filter(status=AppointmentStatus.ACTIVE.value)
    res = []
    for appointment in appointments:
        orders = Order.objects.filter(appointment=appointment).order_by('-created_at')
        total_amount = orders.aggregate(Sum('amount'))['amount__sum'] or 0
        orders_data = []
        for order in orders:
            order_data = {
                "material": order.material.name,
                "quantity": order.quantity,
                "assessed_quantity": order.assessed_quantity,
                "amount": order.amount,
            }
            orders_data.append(order_data)
        appt = {
            "id": appointment.id,
            "description": appointment.description,
            "date": appointment.date,
            "time": appointment.time,
            "address": appointment.address,
            "total_amount": total_amount,
            "status": appointment.status,
            "orders": orders_data
        }

        res.append(appt)

    context = {
        'appointments': res
    }
    print(context)
    return render(request, 'employee/appointment.html', context)