from jobs.models import Venues, VenueDict
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
import json


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
    all_venues_dict = []

    for venue in all_venues:
        new_venue = dict(VenueDict(
            venue['venue_name'],
            venue['status'],
            venue['cam_url'],
            venue['last_updated'],
            venue['sync_time']))
        all_venues_dict.append(new_venue)

    data = {
        "title": "Venues",
        "venues": all_venues_dict,
        "venue_active": "active",
    }
    return render(request, 'venues.html', data)


def cas(request):
    all_venues = Venues.objects.all()
    json_data = json.loads(all_venues.to_json())
    transformed_data = []

    for data in json_data:
        data['ca_name'] = data['venue_name']
        data['time_since_last_update'] = int(datetime.utcnow().timestamp() - (data['last_updated']['$date']/1000))
        del data['_id']
        del data['venue_name']
        del data['cam_url']
        del data['status']
        del data['last_updated']
        del data['sync_time']
        transformed_data.append(data)

    return HttpResponse(json.dumps(transformed_data), content_type='application/json')

