from django import forms
from .models import User, PersonalDetails

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        # fields = '__all__'