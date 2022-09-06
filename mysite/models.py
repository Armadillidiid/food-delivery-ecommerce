from calendar import c
from email.policy import default
from enum import unique
from random import choices
from statistics import mode
from tkinter import CASCADE
from tkinter.ttk import Widget
from django.db import models
from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_order = models.DateField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name


class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    number = PhoneNumberField()
    date_added = models.DateField(auto_now_add=True)


class Vendor(models.Model):
    CATEGORY_CHOICES = [
        ('african', 'African'),
        ('alcoholic drinks', 'Alcoholic Drinks'),
        ('bakery and cakes', 'Bakery and Cakes'),
        ('breakfast', 'Breakfast'),
        ('chinese', 'Chinese'),
        ('fast food', 'Fast Food'),
        ('grills', 'Grills'),
        ('ice cream', 'Ice Cream'),
        ('pizza', 'Pizza'),
        ('vegan', 'Vegan'),
    ]

    name = models.CharField(max_length=200)
    ratings = models.FloatField(default=0)
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
     

class OpenHour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    open_time = models.TimeField()
    close_time = models.TimeField()
    weekday = models.IntegerField()


