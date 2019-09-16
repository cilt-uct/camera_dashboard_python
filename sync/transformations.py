import json
from jobs.models import Venues, VenueDict
from datetime import datetime


def dashboard_data(filter):
    all_venues = Venues.objects.all()
    online_venues = [a for a in all_venues if a["cam_url"]]
    offline_venues = [a for a in all_venues if not a["cam_url"]]
    venues = all_venues

    if filter == 'online':
        venues = online_venues
    elif filter == 'offline':
        venues = offline_venues

    return {
        "title": "Camera Dashboard",
        "venues": venues,
        "dash_active": "active",
        "venue_length": len(all_venues),
        "venue_online": len(online_venues),
        "venue_offline": len(offline_venues),
    }


def venues_data():
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

    return {
        "title": "Venues",
        "venues": all_venues_dict,
        "venue_active": "active",
    }


def ca_json():
    all_venues = Venues.objects.all()
    json_data = json.loads(all_venues.to_json())
    transformed_data = []

    for data in json_data:
        data['ca_name'] = data['venue_name']
        data['time_since_last_update'] = int(datetime.utcnow().timestamp() - (data['last_updated']['$date'] / 1000))
        del data['_id']
        del data['venue_name']
        del data['cam_url']
        del data['status']
        del data['last_updated']
        del data['sync_time']
        transformed_data.append(data)

    return json.dumps(transformed_data)
