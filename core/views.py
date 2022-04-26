from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import AddEmployeeForm, TopupForm
from .models import Employee, Payment
from django.conf import settings
import requests


@login_required(login_url='/accounts/login/')
def index(request):
    my_profile = request.user.profile.first()
    my_company = my_profile.manages
    my_wallet = my_company.wallet.first()
    employees = my_company.employee.all()
    my_transactions = Payment.objects.filter(payment_from=my_company).order_by('-date')[:5][::-1]
    context = {
        'wallet': my_wallet,
        'employees': employees,
        'company': my_company,
        'profile': my_profile,
        'transactions': my_transactions,
    }

    return render(request, 'core/index.html', context)


"""
This function is used to 
"""


def register_employee(request):
    msg = None
    success = False

    if request.method == "POST":
        form = AddEmployeeForm(request.POST)
        if form.is_valid():
            company_ = request.user.profile.first().manages
            Employee.objects.create(
                company=company_,
                name=request.POST['fullname'],
                email=request.POST['email'],
                phone=request.POST['phone']
            )

            msg = 'Employee Registered'
            success = True
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            msg = 'Form is not valid'
    else:
        form = AddEmployeeForm()

    return render(request, "company/register_employee.html", {"form": form, "msg": msg, "success": success})


def view_transaction(request):
    my_company = request.user.profile.first().manages
    my_transactions = my_company.transactions.all()

    context = {
        "transactions": my_transactions
    }

    return render(request, "company/transaction_list.html", context)


def billing(request):
    return render(request, "company/billing.html")


def single_topup(request):
    details = settings.SMS_API
    print(details)
    if request.method == "POST":
        form = TopupForm(request.POST)
        if form.is_valid():
            phone = request.POST['phone']

            request_string = "*804#"
            url = details['server'] + "/services/send-ussd-request.php"
            args = {
                'key': details['api_key'],
                'request': request_string,
                'device': '5028',
                'sim': '1'
            }
            r = requests.get(url=url, params=args)
            data = r.json()
            print(data)
    else:
        form = TopupForm()
    return render(request, "company/topup.html", {"form": form,})


def bulk_topup(request):
    pass
