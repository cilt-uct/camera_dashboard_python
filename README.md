#Camera Dashboard

In order to run camera dashboard you will need to first create a config file (config.py)
in the root directory. It should look as follows:

    //do not change directory
    DIRECTORY = "sync/static/feeds/"

    DIGEST_AUTH = {
        "username": "my_usename",
        "password": "my_password"
    }
    
    //list with the key as the username and value as the password
    BASICAUTH_USERS_LIST = {"username": "password"}
    
    CAPTURE_AGENT_URL = "https://opencast.org/capture-admin/agents.json"

You can run the following command `cp config-dist.py config.py` and change the appropriate values.
 
After creating the config file run `docker-compose up`.

This should build and start up the app.