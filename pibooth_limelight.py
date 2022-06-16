import json
import logging
from http import HTTPStatus

import pibooth
import requests

from pibooth.utils import LOGGER

__version__ = "0.0.1"

PROJECT_NAME = "Limelight"
logger = logging.getLogger(PROJECT_NAME)

# Do not edit, set these in the config file
CONFIG_SECTION = PROJECT_NAME.upper()

LIMELIGHT_SERVER_URL = ""
LIMELIGHT_SERVER_PUT_ENDPOINT = ""
LIMELIGHT_SERVER_POST_ENDPOINT = ""


def get_put_endpoint(id):
    # return f"images/{id}/content"
    return LIMELIGHT_SERVER_PUT_ENDPOINT.format(id)


def get_put_url(id):
    return LIMELIGHT_SERVER_URL + get_put_endpoint(id)


def get_post_endpoint():
    return LIMELIGHT_SERVER_POST_ENDPOINT


def upload_photo(photo_path):
    logger.info(f"Beginning upload procedure for photo ({photo_path})")
    entity_id = do_post()


def do_post():
    url = "http://127.0.0.1:8080/images/"
    payload = "{}"
    headers = {"Content-Type": "application/hal+json"}

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code != HTTPStatus.CREATED:
        logger.error(f"HTTP error: {response.status_code}")
    else:
        logger.info("Image entity created successfully")
        return get_id_from_entity_json(response.json())


def get_id_from_entity_json(json):
    json.get("id")


def do_put(photo_path, id):
    file = {"file": open(photo_path, 'rb')}

    #TODO: swap for url generator function
    url = f"http://127.0.0.1:8080/images/{id}/content"

    payload = {}
    files = [
        ('file', ('photo.jpg', open(photo_path, 'rb'), 'image/jpeg'))
    ]
    headers = {}

    response = requests.put(url, headers=headers, data=payload, files=files)

    if response.status_code == HTTPStatus.OK:
        logger.info(f"Uploaded image successfully with id {id}")
    else:
        logger.error(f"HTTP error: {response.status_code}")

@pibooth.hookimpl
def pibooth_configure(cfg):
    """Set variables for Limelight endpoint access"""
    logger.info("Configuring Limelight for Pibooth...")

    LIMELIGHT_SERVER_URL_DEFAULT = "http://127.0.0.1:8080/"
    LIMELIGHT_SERVER_PUT_ENDPOINT_DEFAULT = "images/{}/content"
    LIMELIGHT_SERVER_POST_ENDPOINT_DEFAULT = "images"

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
    logger.debug("pibooth_startup hook caught by Limelight")

    LIMELIGHT_SERVER_URL = cfg.get(CONFIG_SECTION, "server_url")
    LIMELIGHT_SERVER_POST_ENDPOINT = cfg.get(CONFIG_SECTION, "image_post_endpoint")
    LIMELIGHT_SERVER_PUT_ENDPOINT = cfg.get(CONFIG_SECTION, "image_put_endpoint")

    logger.info(f"LL Server URL: {LIMELIGHT_SERVER_URL}")
    logger.info(f"LL image post endpoint: {LIMELIGHT_SERVER_POST_ENDPOINT}")
    logger.info(f"LL image put endpoint: {LIMELIGHT_SERVER_PUT_ENDPOINT}")
    logger.info(f"LL image post URL: {LIMELIGHT_SERVER_URL + LIMELIGHT_SERVER_POST_ENDPOINT}")
    logger.info(f"LL image put URL: {LIMELIGHT_SERVER_URL + get_put_endpoint('id')}")

    # TODO: remove debug strings
    # logger.info(f"{get_put_endpoint(4)}")
    # logger.info(f"{get_put_endpoint(7)}")


@pibooth.hookimpl
def state_processing_exit(app, cfg):
    logger.debug("state_processing_exit hook caught by Limelight")
    upload_photo(app.previous_picture_file)
