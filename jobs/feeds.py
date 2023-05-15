import os
from celery import shared_task
from .models import Venues
from .utils import *
from config import DIRECTORY
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def get_feeds():
    all_venues = Venues.objects.all()
    logger.info(f'fetched {all_venues.count()} venues from the database')
    check_and_stop_running_processes()

    for venue in all_venues:
        venue_name = venue["venue_name"]

        if contains_unusual_characters(venue_name):
            logger.warn("Could not create the venue {} as it contained special characters".format(venue_name))
            continue

        make_directory("tmp/")

        if check_if_folders_exist(venue_name):
            command = str("openRTSP -F " + "tmp/" + venue_name + " -d 10 -b 400000 " + venue["cam_url"] + " >/dev/null 2>&1"
                          + " && ffmpeg -hide_banner -y -i " + "tmp/" + venue_name + "video-H264-1 -r 1 -vframes 1"
                          + " -f image2 " + DIRECTORY + venue_name + "/" + venue_name
                          + "_big.jpeg >/dev/null 2>&1 && ffmpeg -hide_banner -y -i " + DIRECTORY + venue_name
                          + "/" + venue_name + "_big.jpeg -s 320x180 -f image2 " + DIRECTORY
                          + venue_name + "/" + venue_name + ".jpeg && rm -f " + "tmp/" + venue_name + "* >/dev/null 2>&1")

            logger.info(f'Starting the fetch of lecture recording captures for {venue_name}.')
            run_command.delay(command, venue_name)
        else:
            logger.warn("Unable to run any commands for {}".format(venue_name))


@shared_task
def run_command(command, venue_name):
    logger.info("Running command for {}".format(venue_name))
    os.system(command)

    if check_if_files_exist(venue_name):
        logger.info("Updating timestamp for: {}.".format(venue_name))
        Venues.objects(venue_name=venue_name).update_one(last_updated=get_timestamp(venue_name))
