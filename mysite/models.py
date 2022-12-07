from calendar import c
from contextlib import nullcontext
from email.policy import default
from enum import unique
from hashlib import blake2b
from random import choices
from statistics import mode
from tkinter import CASCADE
from tkinter.ttk import Widget
from unicodedata import category
from unittest.util import _MAX_LENGTH
from wsgiref.validate import validator
from django.db import models
from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image
from sqlalchemy import null
import requests
from .modules.helpers import createCategory

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Vendor(models.Model):
    STATE_CHOICE = [
        ('abia', 'Abia'),
        ('abuja', 'Abuja'),
        ('adamawa', 'Adamawa'),
        ('akwa ibom', 'Akwa Ibom'),
        ('anambra', 'Anambra'),
        ('bauchi', 'Bauchi'),
        ('bayelsa', 'Bayelsa'),
        ('benue', 'Benue'),
        ('borno', 'Borno'),
        ('cross river', 'Cross River'),
        ('delta', 'Delta'),
        ('ebonyi', 'Ebonyi'),
        ('edo', 'Edo'),
        ('ekiti', 'Ekiti'),
        ('enugu', 'Enugu'),
        ('gombe', 'Gombe'),
        ('imo', 'Imo'),
        ('jigawa', 'Jigawa'),
        ('kaduna', 'Kaduna'),
        ('kano', 'Kano'),
        ('katsina', 'Katsina'),
        ('kebbi', 'Kebbi'),
        ('kogi', 'Kogi'),
        ('kwara', 'Kwara'),
        ('lagos', 'Lagos'),
        ('nasarawa', 'Nasarawa'),
        ('niger', 'Niger'),
        ('ogun', 'Ogun'),
        ('ondo', 'Ondo'),
        ('osun', 'Osun'),
        ('oyo', 'Oyo'),
        ('plateau', 'Plateau'),
        ('rivers', 'Rivers'),
        ('sokoto', 'Sokoto'),
        ('taraba', 'Taraba'),
        ('yobe', 'Yobe'),
        ('zamfara', 'Zamfara')
    ]


    # url = "https://locus.fkkas.com/api/states"
    # res = requests.get(url)
    # data = res.json()
    # for state in data['data']:
    #     print(state['alias'], state['alias'].capitalize())
    #     STATE_CHOICE.append((state['alias'], state['alias'].capitalize()))

    CATEGORY_CHOICES = createCategory()

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=200, unique=True) 
    ratings = models.FloatField(default=0)
    location = models.CharField(max_length=200)
    state = models.CharField(max_length=100, choices=STATE_CHOICE, default='abia')
    min_delivery_time = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(60)], null=True)
    max_delivery_time = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(60)], null=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    banner_image = models.ImageField(null=True, blank=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)


    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def bannerURL(self):
        try:
            url = self.banner_image.url
        except:
            url = ''
        return url

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            # if img.width > 200 or img.height > 360:
            output_size = (300, 200)
            new_img = img.resize(output_size)
            new_img.save(self.image.path)


class ProductCategory(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def save(self, *args, **kwargs):
        if self.image:
            super().save(*args, **kwargs)
            img = Image.open(self.image.path)
            if img.width > 200 or img.height > 360:
                output_size = (360, 200)
                img.thumbnail(output_size)
                img.save(self.image.path)

                
class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    contact_name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip_code = models.PositiveIntegerField(null=True, blank=True, validators=[MaxValueValidator(999999)])
    number = PhoneNumberField()
    date_added = models.DateField(auto_now_add=True)


class ShippingAddressOrder(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    contact_name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip_code = models.PositiveIntegerField(null=True, blank=True, validators=[MaxValueValidator(999999999999)])
    number = PhoneNumberField()
    date_added = models.DateField(auto_now_add=True)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    shipping_address = models.ForeignKey(ShippingAddressOrder , on_delete=models.SET_NULL, null=True, blank=True)
    date_order = models.DateTimeField(auto_now=True)
    is_complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100)

    @property
    def get_cart_price(self):
        items = self.orderitem_set.all()
        total = 0
        for item in items:
            total += item.product.price * item.quantity
        return total

    @property
    def get_cart_quantity(self):
        items = self.orderitem_set.all()
        total = 0
        for item in items:
            total += item.quantity
        return total

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name

     

class OpenHour(models.Model):
    CATEGORY_CHOICES = [
        ('Sun', 'Sunday'),
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday')
    ]

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    open_time = models.TimeField()
    close_time = models.TimeField()
    weekday = models.CharField(max_length=100, choices=CATEGORY_CHOICES)






