import pibooth
import requests
from pibooth.utils import LOGGER

__version__ = "0.0.1"

# Do not edit, set these in the config file
CONFIG_SECTION = "LIMELIGHT"
LIMELIGHT_SERVER_URL_DEFAULT = "http://127.0.0.1:8080/"

# TODO: Work out where we're gonna concat this
LIMELIGHT_SERVER_PUT_ENDPOINT_DEFAULT = "images/1/content"
LIMELIGHT_SERVER_POST_ENDPOINT_DEFAULT = "images"
LIMELIGHT_SERVER_URL = ""
LIMELIGHT_SERVER_PUT_ENDPOINT = ""
LIMELIGHT_SERVER_POST_ENDPOINT = ""

@pibooth.hookimpl
def pibooth_configure(cfg):
    """Set variables for Limelight endpoint access"""
    LOGGER.info("Configuring Limelight for Pibooth...")
    cfg.add_option(
        CONFIG_SECTION,
        "server_url",
        LIMELIGHT_SERVER_URL_DEFAULT,
        "Limelight server's URL (e.g. http://127.0.0.1:8080/). Include trailing slash.",
    )
    cfg.add_option(
        CONFIG_SECTION,
        "image_post_endpoint",
        LIMELIGHT_SERVER_POST_ENDPOINT_DEFAULT,
        "Limelight server's image POST endpoint (e.g. images/). This will be appended to the server URL.",
    )
    cfg.add_option(
        CONFIG_SECTION,
        "image_put_endpoint",
        LIMELIGHT_SERVER_PUT_ENDPOINT_DEFAULT,
        "Limelight server's image PUT endpoint (e.g. images/[id]/content). This will be appended to the server URL.",
    )

@pibooth.hookimpl
def pibooth_startup(cfg, app):
    LIMELIGHT_SERVER_URL = cfg.get(CONFIG_SECTION, "server_url")
    LIMELIGHT_SERVER_POST_ENDPOINT = cfg.get(CONFIG_SECTION, "image_post_endpoint")
    LIMELIGHT_SERVER_PUT_ENDPOINT = cfg.get(CONFIG_SECTION, "image_put_endpoint")


    LOGGER.info(f"LL Server URL: {LIMELIGHT_SERVER_URL}")
    LOGGER.info(f"LL image post endpoint: {LIMELIGHT_SERVER_POST_ENDPOINT}")
    LOGGER.info(f"LL image put endpoint: {LIMELIGHT_SERVER_PUT_ENDPOINT}")
    LOGGER.info(f"LL image post URL: {LIMELIGHT_SERVER_URL + LIMELIGHT_SERVER_POST_ENDPOINT}")
    LOGGER.info(f"LL image put URL: {image_put_url}")


@pibooth.hookimpl
def state_processing_exit(app, cfg):
    LOGGER.info("This would be where we'd upload to LL server!")

    upload_photo(app.previous_picture_file, LIMELIGHT_SERVER_POST_URL, LIMELIGHT_SERVER_PUT_URL)


def upload_photo(photo_path, id):
    file = {"file": open(photo_path, 'rb')}

    response = requests.post(LIMELIGHT_SERVER_URL_DEFAULT, file)

    if response.status_code == 200:
        print("Success!")
    else:
        print(f"Failure: {response.status_code}")