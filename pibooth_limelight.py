import pibooth
from pibooth.utils import LOGGER

__version__ = "0.0.1"

CONFIG_SECTION = "LIMELIGHT"
LIMELIGHT_SERVER_URL_DEFAULT = "http://127.0.0.1:8080/"
LIMELIGHT_SERVER_PUT_ENDPOINT_DEFAULT = "images/1/content"
LIMELIGHT_SERVER_POST_ENDPOINT_DEFAULT = "images"

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

    pass