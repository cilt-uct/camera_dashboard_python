import os
from datetime import datetime
from config import DIRECTORY
from celery.utils.log import get_task_logger
from .models import Venues


logger = get_task_logger(__name__)


def check_if_files_exist(cam_url, venue_name):
    if cam_url:
        folder_path = DIRECTORY + venue_name + "/"
        file_path = folder_path + venue_name + ".jpeg"

        if os.path.isfile(file_path):
            logger.info("Updating timestamp for: {}.".format(file_path))
            return datetime.fromtimestamp(os.path.getmtime(file_path))

    return datetime.utcnow()


def check_if_folders_exist(venue_name):
    folder_path = DIRECTORY + venue_name + "/"

    if not os.path.isdir(folder_path):
        logger.info("Creating folder: {}.".format(folder_path))
        os.makedirs(folder_path, exist_ok=True)


def check_if_files_and_folders_exist(cam_url, venue_name):
    check_if_folders_exist(venue_name)
    return check_if_files_exist(cam_url, venue_name)


def delete_venues():
    all_venues = Venues.objects.all()
    deleted = all_venues.delete()
    logger.info("Number of deleted venues: {}".format(str(deleted)))


def get_camera_url(items):
    cam_url = ""

    for item in items:
        if item:
            if "rtsp" in item["value"]:
                cam_url = item["value"]
                cam_url = cam_url.replace("rtspt", "rtsp")

    return cam_url


def check_and_stop_running_processes():
    running_procs = os.system('ps aux | grep "[o]penRTSP" | wc -l')

    if int(running_procs) > 0:
        logger.info(
            "There are currently {} running/hanging OpenRTSP processes. Killing them all.".format(running_procs))
        os.system("kill  -9 $(ps aux | grep '[o]penRTSP' | awk '{print $2}') > /var/log/feeds.log 2>&1")
