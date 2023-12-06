from django.db import models
from users.models import User, TimestampedModel
from enum import Enum


# Create your models here.

class AppointmentStatus(Enum):
    EXECUTED = "executed"
    PENDING = "pending"
    REJECTED = "rejected"

class MaterialUnits(Enum):
    KILOGRAM = "kilogram"
    GRAM = "gram"

class Material(TimestampedModel):
    name = models.CharField(max_length=20)
    unit = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in MaterialUnits], default=MaterialUnits.GRAM.value)
    rate = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.rate}/{self.unit})"

class Appointment(TimestampedModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    materials = models.ManyToManyField(Material)
    status = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in AppointmentStatus], default=AppointmentStatus.PENDING.value)


class Order(TimestampedModel):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount = models.FloatField()
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)

class Payment(TimestampedModel):
    amount = models.FloatField()
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    received_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_by")
    confirmed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="confirmed_by")

