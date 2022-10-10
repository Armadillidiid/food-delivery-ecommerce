from django import forms
from django.forms import EmailField, ModelForm
from .models import User, ShippingAddress
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class MyUserCreationForm(ModelForm):
    class Meta:
        model = User
        widgets = {
            'password' : forms.PasswordInput(),
            'phone_number' : PhoneNumberPrefixWidget(initial='NG')
        }
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']


class ShippingAddressForm(ModelForm):
    class Meta:
        model = ShippingAddress
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Name / Building / Apartment No'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ikeja'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lagos'}),
            'number': PhoneNumberPrefixWidget(initial='NG', attrs={'class': 'form-control w-auto', 'placeholder': '8008008000'})
        }
        fields = '__all__'
        exclude = ['customer']
