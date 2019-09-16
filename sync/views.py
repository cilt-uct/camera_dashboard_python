from django.shortcuts import render
from django.http import HttpResponse
from .transformations import *


def dashboard(request):
    data = dashboard_data(filter="")
    return render(request, 'dashboard.html', data)


def online(request):
    data = dashboard_data(filter="online")
    return render(request, 'dashboard.html', data)


def offline(request):
    data = dashboard_data(filter="offline")
    return render(request, 'dashboard.html', data)


def venues(request):
    data = venues_data()
    return render(request, 'venues.html', data)


def cas(request):
    data = ca_json()
    return HttpResponse(data, content_type='application/json')
