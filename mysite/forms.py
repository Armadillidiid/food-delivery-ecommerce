from django import forms
from django.forms import EmailField, ModelForm
from .models import *
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
            'contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bill Cosby'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Name / Building / Apartment No'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ikeja'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lagos'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '902100'}),
            'number': PhoneNumberPrefixWidget(initial='NG', attrs={'class': 'form-control w-auto', 'placeholder': '8008008000'}),
            'db_id': forms.TextInput()
        }
        fields = '__all__'
        exclude = ['customer']
    

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        widgets = { 
            'first_name': forms.TextInput(attrs={'class': 'form-control w-25'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control w-25'}),
            'email': forms.TextInput(attrs={'class': 'form-control w-25'}),
            'phone_number' : PhoneNumberPrefixWidget(initial='NG', attrs={'class': 'form-control w-auto'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control w-25'}),
        }
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']


class registerVendorForm(ModelForm):
    class Meta:
        model = Vendor
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control merchant-panel-form border-0 w-25', 'placeholder': 'Name'}),
            'location': forms.TextInput(attrs={'class': 'form-control merchant-panel-form border-0 w-25', 'placeholder': 'Location'}),
            'state': forms.Select(attrs={'class': 'form-control merchant-panel-form border-0 w-25'}),
            'min_delivery_time': forms.NumberInput(attrs={'class': 'form-control merchant-panel-form border-0 w-25'}),
            'max_delivery_time': forms.NumberInput(attrs={'class': 'form-control merchant-panel-form border-0 w-25'}),
            'category': forms.Select(attrs={'class': 'form-control merchant-panel-form border-0 w-25'}),
            'image': forms.FileInput(attrs={'class': 'form-control merchant-panel-form border-0 w-25'}),
            'banner_image': forms.FileInput(attrs={'class': 'form-control merchant-panel-form border-0 w-25'}),
        }
        fields = ['name', 'location', 'state', 'min_delivery_time', 'max_delivery_time', 'category', 'image', 'banner_image', 'user']