from django.contrib import admin
from . models import *

# Register your models here.

admin.site.register(Material)
admin.site.register(Order)
admin.site.register(Appointment)
admin.site.register(Payment)