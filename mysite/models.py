from enum import unique
from random import choices
from statistics import mode
from tkinter.ttk import Widget
from django.db import models
from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=50, null=True, blank=True)
    # first_name = models.CharField(max_length=25)
    # last_name  = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(null=True)
    # # password = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

