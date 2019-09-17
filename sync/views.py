from django.shortcuts import render
from django.http import HttpResponse
from .transformations import *
from basicauth.decorators import basic_auth_required


@basic_auth_required
def dashboard(request):
    data = dashboard_data(filter="")
    return render(request, 'dashboard.html', data)


@basic_auth_required
def online(request):
    data = dashboard_data(filter="online")
    return render(request, 'dashboard.html', data)


@basic_auth_required
def offline(request):
    data = dashboard_data(filter="offline")
    return render(request, 'dashboard.html', data)


@basic_auth_required
def venues(request):
    data = venues_data()
    return render(request, 'venues.html', data)


@basic_auth_required
def cas(request):
    data = ca_json()
    return HttpResponse(data, content_type='application/json')
