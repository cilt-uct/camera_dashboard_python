import json
from jobs.models import Venues, VenueDict, regularly_updating_check
from datetime import datetime
from jobs.utils import check_if_files_exist, get_timestamp


def dashboard_data(selected_filter):
    all_venues = Venues.objects.all()
    valid_venues = [a for a in all_venues if a["cam_url"]]
    online_venues = []
    offline_venues = []
    venues = valid_venues

    for venue in valid_venues:
        name = venue["venue_name"]
        if check_if_files_exist(name):
            time = get_timestamp(name)
            if not regularly_updating_check(time):
                offline_venues.append(venue)
            else:
                online_venues.append(venue)

    if selected_filter == 'online':
        venues = online_venues
    elif selected_filter == 'offline':
        venues = offline_venues

    return {
        "title": "Camera Dashboard",
        "venues": venues,
        "dash_active": "active",
        "venue_length": len(valid_venues),
        "venue_online": len(online_venues),
        "venue_offline": len(offline_venues),
    }


def venues_data():
    all_venues = Venues.objects.all()
    valid_venues = [a for a in all_venues if a["cam_url"]]
    all_venues_dict = []

    for venue in valid_venues:
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
    valid_venues = [a for a in json_data if a["cam_url"]]
    transformed_data = []

    for data in valid_venues:
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
