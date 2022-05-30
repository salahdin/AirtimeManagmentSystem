import csv
import datetime
import io

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from django.contrib import messages
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from .forms import AddEmployeeForm, TopupForm, BulkTopupForm
from .models import Employee, Payment
from .notification import send_sms


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


@login_required(login_url='/accounts/login/')
def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    transactions = employee.payments.all()
    context = {
        'employee': employee,
        'transactions': transactions
    }
    return render(request, 'company/employee_detail.html', context)


@login_required(login_url='/accounts/login/')
def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/accounts/login/')
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


@login_required(login_url='/accounts/login/')
def view_transaction(request):
    my_company = request.user.profile.first().manages
    my_transactions = my_company.transactions.all()
    my_wallet = my_company.wallet.first()

    context = {
        "transactions": my_transactions,
        "company": my_company,
        "wallet": my_wallet
    }

    return render(request, "company/transaction_list.html", context)


def billing(request):
    return render(request, "company/billing.html")


@login_required(login_url='/accounts/login/')
def single_topup(request, employee_id):
    msg = None
    success = False
    details = settings.SMS_API
    my_profile = request.user.profile.first()
    my_company = my_profile.manages
    my_wallet = my_company.wallet.first()
    if request.method == "POST":
        form = TopupForm(request.POST)
        if form.is_valid():
            phone = request.POST['phone']
            amount = float(request.POST['amount'])
            if amount > my_wallet.balance:
                msg = "You have insufficient balance for the these transaction "
                return render(request, "company/topup.html", {"form": form, "msg": msg, "success": success})

            employee = get_object_or_404(Employee, id=employee_id)
            print(my_wallet.balance)
            my_wallet.balance = my_wallet.balance - amount
            my_wallet.save(update_fields=['balance'])
            print(my_wallet.balance)
            request_string = "*807*" + phone + '#'
            print(request_string)
            url = details['server'] + "/services/send-ussd-request.php"
            args = {
                'key': details['api_key'],
                'request': request_string,
                'device': '5178',
                'sim': '1'
            }
            # r = requests.get(url=url, params=args)
            # data = r.json()
            # track transaction
            msg = "transaction successful"
            success = True
            Payment.objects.create(payment_to=employee,
                                   payment_from=my_company,
                                   amount=amount,
                                   date=datetime.datetime.now())
    else:
        form = TopupForm()
    return render(request, "company/topup.html", {"form": form, "msg": msg, "success": success})


@login_required(login_url='/accounts/login/')
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


@login_required(login_url='/accounts/login/')
def generate_pdf_report(request):
    # Create Bytestream buffer
    buf = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    c.line(66, 72, 66, 60)
    c.drawString(20, 800, "Report generated at " + datetime.datetime.now().strftime('%b %d, %Y %H:%M:%S'))

    # get transactions
    my_company = request.user.profile.first().manages
    my_transactions = my_company.transactions.all()
    mywallet = my_company.wallet.first()

    data = []

    try:
        line = []
        for i in my_transactions:
            payment_from = str(i.payment_from)
            payment_to = str(i.payment_to)
            phone = str(i.payment_to.phone)
            amount = str(i.amount) + ' Birr'
            date = str(i.date)

            # Add this loop's step row into data array
            line += [payment_from, payment_to, phone, amount, date]
            data.append(line)
            line = []
    except:
        pass
    data.append(['From', 'To', 'Phone', 'Amount', 'Date', ])
    data.append(['Current Balance  : ' + str(mywallet.balance), '', '', '', ''])
    width, height = A4

    t = Table(data)
    t.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                           # ('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
                           ('VALIGN', (0, 0), (0, -1), 'TOP'),
                           # ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
                           ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                           ('VALIGN', (1, 1), (1, 1), 'MIDDLE'),
                           ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
                           # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                           # ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                           ]))
    t.wrapOn(c, width, height)

    # Finish Up
    t.drawOn(c, 100, 100)
    # c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename="report.pdf")


def upload_employees(request):
    my_company = request.user.profile.first().manages
    if request.method == "POST":
        paramFile = request.FILES['employeefile']
        data_set = paramFile.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        try:
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                _, created = Employee.objects.update_or_create(
                    name=column[0],
                    company=my_company,
                    phone=column[1],
                    email=column[2]
                )
                messages.success(request, 'Employee Imported successfully')
        except Exception:
            messages.warning(request, 'Failed to create account')
    return render(request, "company/bulk_employee.html")
