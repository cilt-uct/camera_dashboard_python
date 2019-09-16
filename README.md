#Camera Dashboard

In order to run camera dashboard you will need to first create a config file (config.py)
in the root directory. It should look as follows:

    //do not change directory
    DIRECTORY = "sync/static/feeds/"

    DIGEST_AUTH = {
        "username": "my_usename",
        "password": "my_password"
    }

After creating the config file run `docker-compose up`.