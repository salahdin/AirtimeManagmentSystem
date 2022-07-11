from django.contrib import admin
from .models import Employee, Wallet, Company, Payment, Config


class EmployeeInline(admin.StackedInline):
    model = Employee


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    list_filter = ['name', ]
    inlines = [EmployeeInline]
    search_fields = ['name', 'address', ]

    class Meta:
        model = Company


admin.site.register(Employee)
admin.site.register(Wallet)
admin.site.register(Company,CompanyAdmin)
admin.site.register(Payment)
admin.site.register(Config)
