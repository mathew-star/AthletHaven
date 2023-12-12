# forms.py

from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from accounts.models import CustomUser
import re

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=30)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone_number', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValidationError('Invalid email format. Example: example@gmail.com')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password1')

        if not any(char.isupper() for char in password):
            raise ValidationError("Passwords should contain at least one uppercase letter.")

        if not any(char.islower() for char in password):
            raise ValidationError("Passwords should contain at least one lowercase letter.")

        if not any(char.isdigit() for char in password):
            raise ValidationError("Passwords should contain at least one digit.")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Passwords should contain at least one special character.")

        return password

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not re.match(r'^[0-9]+$', phone_number):
            raise ValidationError('Phone number must contain only digits.')
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")

        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        # Add 'input' class to all input fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'input'})
        self.fields['password1'].widget.attrs.update({'id': 'id_password'})
        self.fields['password2'].widget.attrs.update({'id': 'id_password'})

