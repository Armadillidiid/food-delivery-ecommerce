from django import forms
from django.forms import ModelForm
from .models import User
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class MyUserCreationForm(ModelForm):
    class Meta:
        model = User
        widgets = {
            'password' : forms.PasswordInput(),
            'phone_number' : PhoneNumberPrefixWidget(initial='NG')
        }
        fields = '__all__'
