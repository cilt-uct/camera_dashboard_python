from django.shortcuts import render
from django.http import HttpResponse
from .transformations import dashboard_data, venues_data, ca_json


def dashboard(request):
    data = dashboard_data()
    return render(request, 'dashboard.html', data)


def venues(request):
    data = venues_data()
    return render(request, 'venues.html', data)


def cas(request):
    data = ca_json()
    return HttpResponse(data, content_type='application/json')
