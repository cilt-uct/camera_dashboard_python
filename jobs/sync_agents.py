import json
import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from requests.auth import HTTPDigestAuth

from config import DIGEST_AUTH, CAPTURE_AGENT_URL
from .models import Venues
from .utils import delete_venues, contains_unusual_characters
from .transformations import create_venue

logger = get_task_logger(__name__)


@shared_task
def do_sync():
    auth = HTTPDigestAuth(DIGEST_AUTH["username"], DIGEST_AUTH["password"])
    url = CAPTURE_AGENT_URL
    params = {"X-Requested-Auth": "Digest"}
    agents = {}

    try:
        response = requests.get(url, auth=auth, headers=params)
        data = json.loads(response.text)
        agents = data["agents"]["agent"]
        logger.info("Number of agents {}.".format(len(agents)))
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

            venue = create_venue(agent)

            Venues.objects.create(**venue)

            number_of_venues += 1

        logger.info("{} venues have been inserted into the database.".format(number_of_venues))
