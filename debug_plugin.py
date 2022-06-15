import pibooth
from pibooth.utils import LOGGER

@pibooth.hookimpl
def pibooth_configure(cfg):
    LOGGER.debug("debug string")
    LOGGER.info("info string")