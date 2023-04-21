import logging

# Create a logger object
logger = logging.getLogger()

# Create a formatter object with a parse format string
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S')

# Create a handler object and set its formatter to the one we just created
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

# Parse a log message
parsed = logging.makeLogRecord({'msg': 'INFO Test message', 'levelno': logging.INFO})

# Log the parsed message
logger.handle(parsed)
