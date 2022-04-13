from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import AddEmployeeForm
from .models import Employee

@login_required(login_url='/accounts/login/')
def index(request):
    my_profile = request.user.profile.first()
    my_company = my_profile.manages
    my_wallet = my_company.wallet.first()
    employees = my_company.employee.all()

    context = {
        'wallet':my_wallet,
        'employees': employees,
        'company': my_company,
        'profile' : my_profile
    }

    return render(request, 'core/index.html', context)


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
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            msg = 'Form is not valid'
    else:
        form = AddEmployeeForm()

    return render(request, "company/register_employee.html", {"form": form, "msg": msg, "success": success})