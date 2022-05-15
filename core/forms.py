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


class TopupForm(forms.Form):
    amount = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": 'Amount',
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


class BulkTopupForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        my_profile = user.profile.first()
        my_company = my_profile.manages
        super(BulkTopupForm, self).__init__(*args, **kwargs)
        self.fields['employees'].queryset = Employee.objects.filter(company=my_company)

    amount = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": 'Amount',
                "class": "form-control"
            }
        ))
    employees = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
    )
