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
            'phone_number' : PhoneNumberPrefixWidget()
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
            'number': PhoneNumberPrefixWidget(initial='NG', attrs={'class': 'form-control', 'placeholder': '8008008000'}),
        }
        fields = '__all__'
        exclude = ['customer']
    

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        widgets = { 
            'first_name': forms.TextInput(attrs={'class': 'form-control profile-form w-100'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control profile-form w-100'}),
            'email': forms.TextInput(attrs={'class': 'form-control profile-form w-100'}),
            'phone_number' : PhoneNumberPrefixWidget(initial='NG', attrs={'class': 'form-control profile-form w-auto'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control profile-form w-100'}),
        }
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']


class registerVendorForm(ModelForm):
    class Meta:
        model = Vendor
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control merchant-panel-form border-0 w-100', 'placeholder': 'Name'}),
            'location': forms.TextInput(attrs={'class': 'form-control merchant-panel-form border-0 w-100', 'placeholder': 'Location'}),
            'state': forms.Select(attrs={'class': 'form-control merchant-panel-form border-0 w-100'}),
            'min_delivery_time': forms.NumberInput(attrs={'class': 'form-control merchant-panel-form border-0 w-100'}),
            'max_delivery_time': forms.NumberInput(attrs={'class': 'form-control merchant-panel-form border-0 w-100'}),
            'category': forms.Select(attrs={'class': 'form-control merchant-panel-form border-0 w-100'}),
            'image': forms.FileInput(attrs={'class': 'form-control merchant-panel-form border-0 w-100'}),
        }
        fields = ['name', 'location', 'state', 'min_delivery_time', 'max_delivery_time', 'category', 'image', 'user']


class selectCategory(ModelForm):    
    class Meta:
        model = Vendor
        widgets = {
            'category': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        fields = ['category']


class OpenHourForm(ModelForm):
    class Meta:
        model = OpenHour
        widgets = {
        'open_time': forms.TimeInput(attrs={'class': 'form-control w-100 merchant-panel-form border-0 openHourOpenTime', 'type': 'time'}),
        'close_time': forms.TimeInput(attrs={'class': 'form-control w-100 merchant-panel-form border-0 openHourCloseTime', 'type': 'time'}),
        'weekday': forms.Select(attrs={'class': 'form-control w-100 merchant-panel-form border-0'})
        }
        fields = ['open_time', 'close_time', 'weekday', 'vendor']


class addProduct(ModelForm):
    class Meta:
        model = Product
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        fields = '__all__'
        exclude = ['vendor', 'category']


class addCategory(ModelForm):
    class Meta:
        model = ProductCategory
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }
        fields = ['name']