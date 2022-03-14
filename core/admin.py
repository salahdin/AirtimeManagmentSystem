from django.contrib import admin
from .models import Employee, Wallet, Company

admin.site.register(Employee)
admin.site.register(Wallet)
admin.site.register(Company)