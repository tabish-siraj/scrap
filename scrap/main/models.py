from django.db import models
from users.models import User, TimestampedModel
from enum import Enum


# Create your models here.

class AppointmentStatus(Enum):
    ACTIVE = "active"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class MaterialUnits(Enum):
    KILOGRAM = "kilogram"
    GRAM = "gram"
    POUND= "pound"
    OUNCE = "ounce"
    

class Material(TimestampedModel):
    name = models.CharField(max_length=20)
    unit = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in MaterialUnits], default=MaterialUnits.GRAM.value)
    rate = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.rate}/{self.unit})"

class Appointment(TimestampedModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee", blank=True, null=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in AppointmentStatus], default=AppointmentStatus.ACTIVE.value)

    def __str__(self):
        return f"{self.customer} - {self.employee}"
class Order(TimestampedModel):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.FloatField()
    assessed_quantity = models.FloatField(blank=True, null=True)    
    amount = models.FloatField()
    assessed_amount = models.FloatField(blank=True, null=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.material} - {self.quantity}"

class ContactUs(TimestampedModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    city = models.CharField(max_length=50)
    contact = models.CharField(max_length=13)
    message = models.TextField()
    
    def __str__(self):
        return self.email