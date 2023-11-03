from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_controller, name='register'),
    path('login/', views.login_controller, name='login'),
    path('logout/', views.logout_controller, name='logout'),
]