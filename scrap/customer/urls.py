from django.urls import path

from . import views

urlpatterns = [
    path("", views.customer_index, name="customer_index"),
    path("edit-profile", views.customer_edit_profile, name="customer_edit_profile"),
    path("create-appointment", views.create_appointment, name="create_appointment"),
]
