from django.shortcuts import render
from main.models import Order, Appointment, Material, AppointmentStatus
from users.models import User, PersonalDetails, VehicleType
from django.db.models import Sum
from django.db import transaction

# Create your views here.
def employee_index(request):
    res = []
    appointments = Appointment.objects.filter(employee=request.user)
    
    for appointment in appointments:
        orders_obj = []
        orders = Order.objects.filter(appointment=appointment)
        total_amount = orders.aggregate(Sum('assessed_amount'))['assessed_amount__sum'] or 0
        for order in orders:
            order_data = {
                "id": order.id,
                "material": order.material.name,
                "rate": order.material.rate,
                "quantity": order.quantity,
                "assessed_quantity": order.assessed_quantity,
                "amount": order.amount,
                "assessed_amount": order.assessed_amount
            }
            orders_obj.append(order_data)
        appt = {
            "id": appointment.id,
            "description": appointment.description,
            "date": appointment.date,
            "time": appointment.time,
            "address": appointment.address,
            "total_amount": total_amount,
            "status": appointment.status,
            "orders": orders_obj,
        }
        res.append(appt)

    context = {
        "appointments": res
    }
    print(context)
    return render(request, 'employee/index.html', context)

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
    appointments = Appointment.objects.filter(employee=request.user, status=AppointmentStatus.ACTIVE.value)
    res = []
    for appointment in appointments:
        orders = Order.objects.filter(appointment=appointment).order_by('-created_at')
        total_amount = orders.aggregate(Sum('amount'))['amount__sum'] or 0
        orders_data = []
        for order in orders:
            order_data = {
                "id": order.id,
                "material": order.material.name,
                "rate": order.material.rate,
                "quantity": order.quantity,
                "assessed_quantity": order.assessed_quantity,
                "amount": order.amount,
                "assessed_amount": order.assessed_amount
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
            "orders": orders_data,
            "statuses": [status.value for status in AppointmentStatus]
        }

        res.append(appt)
    if request.method == "POST":
        with transaction.atomic():
            appointment_id = request.POST.get('appointment_id')
            status = request.POST.get('status')

            appointment = Appointment.objects.filter(id=appointment_id).first()
            if not appointment:
                return render(request, 'employee/appointment.html', {'error': 'Invalid appointment id'})
            
            appointment.status = status
            appointment.save()

            # Process order data
            orders = []
            for order in request.POST:
                if order.startswith('assessed_quantity_'):
                    material = order.replace('assessed_quantity_', '')
                    quantity = request.POST.get(order)
                    order = request.POST.get(f'order_{material}')
                    order_id = order.split('_')[1]
                    rate = request.POST.get(f'rate_{material}')

                    orders.append({'material': material, 'quantity': quantity, 'order_id': order_id, "rate": rate})
            for o in orders:
                order = Order.objects.filter(id=o['order_id']).first()
                if not order:
                    return render(request, 'employee/appointment.html', {'error': 'Invalid order id'})
                order.assessed_quantity = o['quantity']
                amount = float(o['quantity']) * float(o['rate'])
                order.assessed_amount = amount

                order.save()
    context = {
        'appointments': res
    }
    return render(request, 'employee/appointment.html', context)