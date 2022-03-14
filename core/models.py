from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name="company name")
    address = models.CharField(max_length=500, verbose_name="company address")
    logo = models.ImageField(upload_to="element/", blank=True, null=True)
    created = models.DateField(auto_now_add=True)


class Employee(models.Model):
    name = models.CharField(max_length=255, verbose_name="employee name")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employee")
    phone = PhoneNumberField(unique=True)
    email = models.EmailField(blank=True, null=True)


class Wallet(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,
                                 related_name="wallet")
    is_open = models.BooleanField(default=False, verbose_name="is wallet open")
    balance = models.FloatField()
    last_update = models.DateTimeField(auto_now=True)


