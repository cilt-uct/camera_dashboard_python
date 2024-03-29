import json
import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from requests.auth import HTTPDigestAuth

from config import DIGEST_AUTH, CAPTURE_AGENT_URL
from .utils import contains_unusual_characters
from .data_access_layer import create_venue, delete_venues

logger = get_task_logger(__name__)


@shared_task
def do_sync():
    url = CAPTURE_AGENT_URL
    agents = {}

    try:
        if DIGEST_AUTH["username"] and DIGEST_AUTH["password"]:
            params = {"X-Requested-Auth": "Digest"}
            auth = HTTPDigestAuth(DIGEST_AUTH["username"], DIGEST_AUTH["password"])
            response = requests.get(url, auth=auth, headers=params)
        else:
            response = requests.get(url)
        data = json.loads(response.text)
        agents = data["agents"]["agent"]
        logger.info("Number of agents fetched from media JSON: {}.".format(len(agents)))
    except requests.HTTPError as e:
        status_code = e.response.status_code
        logger.error("Failed to fetch capture agents".format(status_code))

    if agents:
        delete_venues()
        number_of_venues = 0

        for agent in agents:
            if not agent["capabilities"]:
                continue

            venue_name = agent["name"]
            if contains_unusual_characters(venue_name):
                logger.warn("Could not create the venue {} as it contained special characters".format(venue_name))
                continue

            create_venue(agent)
            number_of_venues += 1

        logger.info("{} venues have been inserted into the database.".format(number_of_venues))
