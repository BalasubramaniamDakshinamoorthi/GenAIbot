from icecream import install, ic
import logging

log_format = "[%(levelname)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)
logger = logging.getLogger(__name__)


def info(s):
    logger.info(s)


install()
ic.configureOutput(prefix="", outputFunction=info)




