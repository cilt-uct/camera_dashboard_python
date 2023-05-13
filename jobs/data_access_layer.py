from .utils import files_and_folders_exist, get_camera_url, get_timestamp
from datetime import datetime
from .models import Venues
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


def create_venue(agent):
    items = agent["capabilities"]["item"]
    cam_url = get_camera_url(items)

    if not cam_url:
        return

    venue_name = agent["name"]

    venue = {
        'venue_name': venue_name,
        'status': agent["state"],
        'sync_time': datetime.now(),
        'cam_url': cam_url,
        'last_updated': get_timestamp(venue_name) if files_and_folders_exist(venue_name) else datetime.now(),
    }

    create(venue)


def create(venue):
    Venues.objects.create(**venue)


def delete_venues():
    all_venues = Venues.objects.all()
    deleted = all_venues.delete()
    logger.info("Number of deleted venues: {}".format(str(deleted)))
