import os
from celery import shared_task
from .models import Venues
from config import DIRECTORY
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def get_feeds():
    commands = []
    all_venues = Venues.objects.all()
    running_procs = os.system('ps aux | grep "[o]penRTSP" | wc - l')

    if int(running_procs) > 0:
        logger.info("There are currently {} running/hanging OpenRTSP processes. Killing them all.".format(running_procs))
        os.system("killall openRTSP 2>&1 > /dev/null")

    for venue in all_venues:
        folder_path = DIRECTORY + venue["venue_name"] + "/"

        if not os.path.isdir(folder_path):
            logger.info("Creating folder: {}.".format(folder_path))
            os.makedirs(folder_path, exist_ok=True)

        command = str("openRTSP -F " + venue["venue_name"] + " -d 10 -b 400000 " + venue["cam_url"]
                      + " && ffmpeg -y -i " + venue["venue_name"] + "video-H264-1 -r 1 -vframes 1"
                      + " -f image2 " + DIRECTORY + venue["venue_name"] + "/" + venue["venue_name"]
                      + "_big.jpeg && ffmpeg -y -i " + DIRECTORY + venue["venue_name"]
                      + "/" + venue["venue_name"] + "_big.jpeg -s 320x180 -f image2 " + DIRECTORY
                      + venue["venue_name"] + "/" + venue["venue_name"] + ".jpeg && rm -f " + venue["venue_name"] + "*")

        commands.append(command)

    if len(commands) > 0:
        logger.info("Starting the fetch of lecture recording captures.")
        for command in commands:
            run_command.delay(command)
    else:
        logger.info("No commands available, no venue objects in the Database.")


@shared_task
def run_command(command):
    logger.info("RUNNING, {}".format(command))
    os.system(command)
