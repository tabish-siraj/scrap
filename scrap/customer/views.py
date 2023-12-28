from django.db import transaction
from django.shortcuts import render
from django.db.models import Sum
from users.models import User, PersonalDetails, UserType
from main.models import Appointment, Material,Order, AppointmentStatus



# Create your views here.

def customer_index(request):
    appointments = Appointment.objects.filter(customer=request.user)

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
                "assessed_amount": order.assessed_amount,
            }
            orders_data.append(order_data)
        appt = {
                "id": appointment.id,
                "description": appointment.description,
                "date": appointment.date,
                "time": appointment.time,
                "address": appointment.address,
                "status": appointment.status,
                "amount": total_amount,
                "orders": orders_data
            }
        res.append(appt)

    context = {
        "appointments": res
    }
    return render(request, 'customer/index.html', context)

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
        
    return render(request, 'customer/edit_profile.html', context)

def create_appointment(request):
    try:
        with transaction.atomic():
            materials = Material.objects.all()
            personal_detail = PersonalDetails.objects.filter(user=request.user).first()
            context = {}

            if request.method == "POST":
                customer = request.user
                address = request.POST['address']
                city = request.POST['city']
                state = request.POST['state']
                country = request.POST['country']
                contact = request.POST['contact']
                description = request.POST['description']
                date = request.POST['date']
                time = request.POST['time']

                if not customer or not address or not city or not state or not country or not contact or not description or not date or not time:
                    context['error'] = "Please fill all the fields"
                    return render(request, 'customer/create_appointment.html', context)
                
                employee = User.objects.filter(user_type=UserType.EMPLOYEE.value).order_by('?').first()

                appointment = Appointment.objects.create(
                    customer=customer,
                    employee=employee,
                    address=address,
                    city=city,
                    state=state,
                    country=country,
                    contact=contact,
                    description=description,
                    date=date,
                    time=time,
                    status=AppointmentStatus.ACTIVE.value
                )

                orders = []
                for i in range(len(materials)):
                    if request.POST[f'{materials[i].name}_quantity'] == '':
                        continue
                    quantity = request.POST[f'{materials[i].name}_quantity']
                    amount = request.POST[f'{materials[i].name}_total']
                    order = Order.objects.create(
                        appointment=appointment,
                        material=materials[i],
                        quantity=quantity,
                        amount=amount
                    )
                    orders.append(order)
            if  appointment is not None and len(orders) > 0:
                context['success'] = "Appointment created successfully"
    except Exception as e:
        print(str(e))
        context['error'] = "Something went wrong"

    context.update({
        'materials': materials,
        'personal_detail': personal_detail
    })
    return render(request, 'customer/create_appointment.html', context)