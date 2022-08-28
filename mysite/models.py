from enum import unique
from random import choices
from tkinter.ttk import Widget
from django.db import models
from django import forms
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=25)
    last_name  = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True)
    password = models.CharField(max_length=65)