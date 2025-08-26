# Camera Dashboard

The Camera Dashboard displays a view of all the cameras connected to Capture Agents (CA) which in turn are connected to Opencast. The dashboard shows the current status of the CA's and also a snapshot of the camera view, which is updated every 5 minutes.

## Structure

The service consists of 4 parts:
1. Mongo Database (`db`): stores the current state of the Capture Agents.
2. Messaging (`rabbitmq`): used to communicate between the python Django front-end and the scheduling service.
3. Scheduling Service (`celery`, `celery_beat`): the scheduling service runs jobs at certain times to update the status of the CA's in the database and obtain new snapshots from the cameras.
4. Front-End (`cam_dash`): displays the user interface to view the status and snapshots of the capture agents and related cameras.

## Deployment

In order to run camera dashboard you will need to first create a config file (config.py)
in the root directory. It should look as follows:
```
    # list of venues that should not be displayed
    PRIVATE_VENUES = []

    //do not change directory
    DIRECTORY = "sync/static/feeds/"

    DIGEST_AUTH = {
        "username": "",
        "password": ""
    }
    
    CAPTURE_AGENT_URL = "https://stable.opencast.org/capture-admin/agents.json"
```
You can run the following command `cp config-dist.py config.py` and change the appropriate values.
 
After creating the config file run `docker-compose up -d`.

This should build and start up the app.
