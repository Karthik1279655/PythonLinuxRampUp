import logging

LOG_FORMAT = '{asctime} : {levelname} : {message}'

logging.basicConfig(filename='mylog.log',
                    level=logging.ERROR,
                    filemode='w',
                    format=LOG_FORMAT,
                    style='{')

try:
    1 / 0
except ZeroDivisionError as e:
    logging.error("ZeroDivisionError", exc_info=True)
    logging.exception("ZeroDivisionError")
