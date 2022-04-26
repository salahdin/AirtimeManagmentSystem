from django.contrib import admin
from .models import Employee, Wallet, Company,Payment

admin.site.register(Employee)
admin.site.register(Wallet)
admin.site.register(Company)
admin.site.register(Payment)