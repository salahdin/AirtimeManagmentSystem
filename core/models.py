from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name="company name")
    tin_number = models.CharField(max_length=255, verbose_name="company tin number", null=True, blank=True)
    address = models.CharField(max_length=500, verbose_name="company address")
    logo = models.ImageField(upload_to="element/", blank=True, null=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=255, verbose_name="employee name")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employee")
    phone = PhoneNumberField(unique=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name


class Wallet(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                related_name="wallet")
    is_open = models.BooleanField(default=False, verbose_name="is wallet open")
    balance = models.FloatField()
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.company} - {self.balance} Birr'


class Payment(models.Model):
    payment_to = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="payments")
    payment_from = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="transactions")
    amount = models.FloatField()
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.payment_from} -> {self.payment_to} amount of {self.amount} Birr'


class Config(models.Model):
    api_key = models.CharField(max_length=255)
    server = models.CharField(max_length=255)
    sim = models.IntegerField()
    device = models.IntegerField()