from .utils import files_and_folders_exist, get_camera_url, get_timestamp
from datetime import datetime


def create_venue(agent):
    items = agent["capabilities"]["item"]
    cam_url = get_camera_url(items)
    venue_name = agent["name"]

    return {
        'venue_name': venue_name,
        'status': agent["state"],
        'sync_time': datetime.now(),
        'cam_url': cam_url,
        'last_updated': get_timestamp(venue_name) if files_and_folders_exist(venue_name) else datetime.now(),
    }
