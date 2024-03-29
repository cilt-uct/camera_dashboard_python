import os
import re
from datetime import datetime
from config import DIRECTORY
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


def check_if_files_exist(venue_name):
    file_path = get_file_path(venue_name)
    if os.path.isfile(file_path):
        return True

    return False


def check_if_folders_exist(venue_name):
    folder_path = DIRECTORY + venue_name + "/"

    try:
        make_directory(folder_path)
    except Exception as e:
        logger.error("Could not create folder: {}.".format(str(e)))
        return False

    return True


def make_directory(folder_path):
    if not os.path.isdir(folder_path):
        logger.info("Creating folder: {}.".format(folder_path))
        os.makedirs(folder_path, exist_ok=True)


def get_timestamp(venue_name):
    try:
        file_path = get_file_path(venue_name)
        return datetime.fromtimestamp(os.path.getmtime(file_path))
    except:
        logger.warn("Failed to fetch timestamp. File might not be available.")


def files_and_folders_exist(venue_name):
    if check_if_folders_exist(venue_name) and check_if_files_exist(venue_name):
        return True

    return False


def get_file_path(venue_name):
    folder_path = DIRECTORY + venue_name + "/"
    return folder_path + venue_name + ".jpeg"


def get_camera_url(items):
    cam_url = ""

    if isinstance(items, dict):
        if "rtsp" in items["value"]:
            cam_url = items["value"]
            cam_url = cam_url.replace("rtspt", "rtsp")

        return cam_url

    for item in items:
        try:
            if item:
                if "rtsp" in item["value"]:
                    cam_url = item["value"]
                    cam_url = cam_url.replace("rtspt", "rtsp")
        except Exception as e:
            logger.error(f'Something went wrong while attempting to get the url in {str(items)}, error: {str(e)}')
            return None

    return cam_url


def check_and_stop_running_processes():
    running_procs = os.system('ps aux | grep "[o]penRTSP" | wc -l')

    if int(running_procs) > 0:
        logger.info(
            "There are currently {} running/hanging OpenRTSP processes. Killing them all.".format(running_procs))
        os.system("kill  -9 $(ps aux | grep '[o]penRTSP' | awk '{print $2}') > /var/log/feeds.log 2>&1")


def contains_unusual_characters(venue_name):
    pattern = re.compile("^[A-Za-z0-9]+$")
    if pattern.match(venue_name):
        return False

    return True
