import requests, json, os
from config import DIGEST_AUTH, DIRECTORY
from requests.auth import HTTPDigestAuth
from celery import shared_task
from datetime import datetime
from .models import Venues


@shared_task
def do_sync():
    auth = HTTPDigestAuth(DIGEST_AUTH["username"], DIGEST_AUTH["password"])
    url = 'https://media.uct.ac.za/capture-admin/agents.json'
    params = {"X-Requested-Auth": "Digest"}

    response = requests.get(url, auth=auth, headers=params)
    data = json.loads(response.text)
    agents = data["agents"]["agent"]

    if agents:
        delete_venues()

        for agent in agents:
            if not agent["capabilities"]:
                continue

            venue_name = agent["name"]
            last_updated = datetime.now()
            items = agent["capabilities"]["item"]
            cam_url = get_camera_url(items)

            if cam_url:
                folder_path = DIRECTORY + venue_name + "/"
                file_path = folder_path + venue_name+".jpeg"

                if not os.path.isdir(folder_path):
                    os.makedirs(folder_path, exist_ok=True)

                if os.path.isfile(file_path):
                    last_updated = os.path.getmtime(file_path)

            Venues.objects.create(
                venue_name=venue_name,
                cam_url=cam_url,
                last_updated=last_updated,
                sync_time=datetime.now
            )


def delete_venues():
    all_venues = Venues.objects.all()
    deleted = all_venues.delete()
    #Todo logging
    print("deleted: " + str(deleted))


def get_camera_url(items):
    cam_url = ""

    for item in items:
        if item:
            if "rtsp" in item["value"]:
                cam_url = item["value"]
                cam_url = cam_url.replace("rtspt", "rtsp")

    return cam_url

