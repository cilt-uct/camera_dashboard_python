from jobs.models import Venues
from django.shortcuts import render


def dashboard(request):
    all_venues = Venues.objects.all()
    data = {
        "title": "Camera Dashboard",
        "venues": all_venues
    }
    return render(request, 'dashboard.html', data)


def tiled(request):
    all_venues = Venues.objects.all()
    return render(request, 'tiled.html')


def venues(request):
    all_venues = Venues.objects.all()
    return render(request, 'venues.html')


def cas():
    print("cas")

