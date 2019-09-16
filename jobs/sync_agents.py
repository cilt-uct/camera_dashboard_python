import json
import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from requests.auth import HTTPDigestAuth

from config import DIGEST_AUTH
from .models import Venues
from .utils import delete_venues
from .transformations import create_venue

logger = get_task_logger(__name__)


@shared_task
def do_sync():
    auth = HTTPDigestAuth(DIGEST_AUTH["username"], DIGEST_AUTH["password"])
    url = 'https://media.uct.ac.za/capture-admin/agents.json'
    params = {"X-Requested-Auth": "Digest"}

    response = requests.get(url, auth=auth, headers=params)
    data = json.loads(response.text)
    agents = data["agents"]["agent"]
    logger.info("Number of agents {}.".format(len(agents)))

    if agents:
        delete_venues()
        number_of_venues = 0

        for agent in agents:
            if not agent["capabilities"]:
                continue

            venue = create_venue(agent)

            Venues.objects.create(**venue)

            number_of_venues += 1

        logger.info("{} venues have been inserted into the database.".format(number_of_venues))
