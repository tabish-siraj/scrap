from django.contrib import admin
from .models import PersonalDetails, User

# Register your models here.

admin.site.register(PersonalDetails)
admin.site.register(User)