import logging
from logging import *

LOG_FORMAT = '{lineno} : {name} : {asctime} : {message}'

basicConfig(filename='logfile.log',
            level=logging.DEBUG,
            filemode='w',
            format=LOG_FORMAT,
            style='{')

logger = getLogger('Geek')

logger.debug("This is Debug")
logger.info("This is Info")
logger.warning("This is Warning")
logger.error("This is Error")
logger.critical("This is Critical")
