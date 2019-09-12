from jobs.models import Venues
from django.shortcuts import render


def dashboard(request):
    all_venues = Venues.objects.all()
    online_venues = [a for a in all_venues if a["cam_url"]]
    data = {
        "title": "Camera Dashboard",
        "venues": all_venues,
        "dash_active": "active",
        "venue_length": len(all_venues),
        "venue_online": len(online_venues),
        "venue_offline": (len(all_venues)-len(online_venues)),
    }
    return render(request, 'dashboard.html', data)


def venues(request):
    all_venues = Venues.objects.all()
    data = {
        "title": "Venues",
        "venues": all_venues,
        "venue_active": "active",
    }
    return render(request, 'venues.html', data)


def cas():
    print("cas")

