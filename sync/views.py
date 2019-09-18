from django.shortcuts import render
from django.http import HttpResponse
from .transformations import *
from basicauth.decorators import basic_auth_required


@basic_auth_required
def dashboard(request):
    data = dashboard_data("")
    return render(request, 'dashboard.html', data)


@basic_auth_required
def online(request):
    data = dashboard_data("online")
    return render(request, 'dashboard.html', data)


@basic_auth_required
def offline(request):
    data = dashboard_data("offline")
    return render(request, 'dashboard.html', data)


@basic_auth_required
def venues(request):
    data = venues_data()
    return render(request, 'venues.html', data)


def cas(request):
    data = ca_json()
    return HttpResponse(data, content_type='application/json')


def robots(request):
    f = open('/camera_dashboard/robots.txt', 'r')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type='application/json')


def humans(request):
    f = open('/camera_dashboard/humans.txt', 'r')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type='application/json')