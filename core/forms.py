from django import forms
from .models import Employee


class AddEmployeeForm(forms.Form):
    fullname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Full Name",
                "class": "form-control"
            }
        ))

    phone = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Phone",
                "class": "form-control"
            }
        ))

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = Employee
        fields = ('name', 'phone', 'email',)
