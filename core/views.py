from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView


@login_required(login_url='/accounts/login/')
def index(request):
    return render(request, 'core/index.html')
