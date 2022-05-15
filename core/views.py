from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AddEmployeeForm, TopupForm, BulkTopupForm
from .models import Employee, Payment
from django.conf import settings
import requests
from .notification import send_sms
import datetime


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
This function is used to add new employees
"""


def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    transactions = employee.payments.all()
    context = {
        'employee': employee,
        'transactions': transactions
    }
    return render(request, 'company/employee_detail.html', context)


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


def single_topup(request, employee_id):
    details = settings.SMS_API
    my_profile = request.user.profile.first()
    my_company = my_profile.manages
    if request.method == "POST":
        form = TopupForm(request.POST)
        if form.is_valid():
            phone = request.POST['phone']
            amount = request.POST['amount']
            employee = get_object_or_404(Employee, id=employee_id)
            print(employee.phone)
            request_string = "*807*" + phone + '#'
            print(request_string)
            url = details['server'] + "/services/send-ussd-request.php"
            args = {
                'key': details['api_key'],
                'request': request_string,
                'device': '5178',
                'sim': '1'
            }
            r = requests.get(url=url, params=args)
            data = r.json()
            # track transaction
            Payment.objects.create(payment_to=employee,
                                   payment_from=my_company,
                                   amount=amount,
                                   date=datetime.datetime.now())
    else:
        form = TopupForm()
    return render(request, "company/topup.html", {"form": form, })


def bulk_topup(request):
    details = settings.SMS_API
    my_profile = request.user.profile.first()
    my_company = my_profile.manages
    if request.method == "POST":
        form = BulkTopupForm(request.POST, user=request.user)
        if form.is_valid():
            # get employees from form
            employees = form.cleaned_data.get("employees")
            amount = request.POST['amount']
            # clean queryset
            final_list = [employee for employee in employees if employee.phone.national_number]
            url = details['server'] + "/services/send-ussd-request.php"
            for employee in final_list:
                request_string = "*807*" + employee.phone.national_number + "#"
                args = {
                    'key': details['api_key'],
                    'request': request_string,
                    'device': '5178',
                    'sim': '2'
                }

                # send api request
                r = requests.get(url=url, params=args)
                # send notification sms
                send_sms(employee.phone.national_number, amount, my_company.name, employee.name)
                # track transaction
                Payment.objects.create(payment_to=employee,
                                       payment_from=my_company,
                                       amount=amount,
                                       date=datetime.datetime.now())
    else:
        form = BulkTopupForm(user=request.user)
    return render(request, "company/bulk_topup.html", {"form": form})


"""def bulk_topup(request):
    details = settings.SMS_API
    my_profile = request.user.profile.first()
    my_company = my_profile.manages
    employees = my_company.employee.all()
    final_list = [employee for employee in employees if employee.phone.national_number]

    for employee in final_list:
        request_string = "*807*" + employee.phone.national_number + "#"
        url = details['server'] + "/services/send-ussd-request.php"
        args = {
            'key': details['api_key'],
            'request': request_string,
            'device': '5178',
        }
        r = requests.get(url=url, params=args)
        #send_sms(phone,amount,my_company.name, employee.name)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))"""
