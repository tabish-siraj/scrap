from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum
from .manager import UserManager

# Create your models here.

class UserType(Enum):
    CUSTOMER = "customer"
    EMPLOYEE = "employee"

class VehicleType(Enum):
    TWO_WHEELER = "two wheeler"
    THREE_WHEELER = "three wheeler"
    FOUR_WHEELER = "four wheeler"

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in UserType], default=UserType.CUSTOMER.value)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.user_type})"
    
    def is_customer(self):
        return self.user_type == UserType.CUSTOMER.value
    
    def is_employee(self):
        return self.user_type == UserType.EMPLOYEE.value
    

class PersonalDetails(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    mobile_number = models.CharField(max_length=13)
    address1 = models.CharField(max_length=100, null=True, blank=True)
    address2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    cnic = models.CharField(max_length=15, null=True, blank=True)
    vehicle_no = models.CharField(max_length=15, null=True, blank=True)
    vehicle_type = models.CharField(max_length=13, null=True, blank=True, choices=[(tag.name, tag.value) for tag in VehicleType])
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.user.email