from django.urls import path
from . import views

urlpatterns = [
    path("", views.employee_index, name="employee_index"),
    path("appointments/", views.employee_appointments, name="employee_appointment"),
    path("edit-profile/", views.employee_edit_profile, name="employee_edit_profile"),
]
