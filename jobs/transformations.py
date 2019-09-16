from .utils import check_if_files_and_folders_exist, get_camera_url
from datetime import datetime


def create_venue(agent):
    items = agent["capabilities"]["item"]
    cam_url = get_camera_url(items)
    venue_name = agent["name"]

    return {
        'venue_name': venue_name,
        'status': agent["state"],
        'sync_time': datetime.utcnow(),
        'cam_url': cam_url,
        'last_updated': check_if_files_and_folders_exist(cam_url, venue_name),
    }
