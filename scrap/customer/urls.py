from django.urls import path

from . import views

urlpatterns = [
    path("", views.customer_index, name="customer_index"),
]
