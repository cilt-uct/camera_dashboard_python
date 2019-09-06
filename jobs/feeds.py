import os
from celery import shared_task
from .models import Venues
from config import DIRECTORY
import billiard.pool as mp
import time


@shared_task
def get_feeds():
    start = time.time()
    print("feeds")

    pool = mp.Pool(100)

    commands = []
    all_venues = Venues.objects.all()
    running_procs = os.system('ps aux | grep "[o]penRTSP" | wc - l')

    if int(running_procs) > 0:
        os.system("killall openRTSP 2>&1 > /dev/null")

    for venue in all_venues:
        folder_path = DIRECTORY + venue["venue_name"] + "/"

        if not os.path.isdir(folder_path):
            os.makedirs(folder_path, exist_ok=True)

        command = ("openRTSP -F " + venue["venue_name"] + " -d 10 -b 400000 " + venue["cam_url"]
                   + " && ffmpeg -y -i " + venue["venue_name"] + "video-H264-1 -r 1 -vframes 1"
                   + " -f image2 " + DIRECTORY + venue["venue_name"] + "/" + venue["venue_name"]
                   + "_big.jpeg && ffmpeg -y -i " + DIRECTORY + venue["venue_name"]
                   + "/" + venue["venue_name"] + "_big.jpeg -s 320x180 -f image2 " + DIRECTORY
                   + venue["venue_name"] + "/" + venue["venue_name"] + ".jpeg && rm -f " + venue["venue_name"] + "*")

        commands.append(command)

    result = pool.map(run_command, commands)
    print(result)
    end = time.time()
    print("Time elapsed", end - start)
    pool.close()
    pool.join()


def run_command(command):
    print("RUNNING, ", command)
    print("Pid: ", os.getpid())
    os.system(command)
