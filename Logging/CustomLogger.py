import logging

logging.basicConfig(filename='mylog.log',
                    level=logging.INFO,
                    filemode='w',
                    format='%(asctime)s : %(levelname) : %(message)')

logger = logging.getLogger(__name__)

handler = logging.FileHandler('test.log')

formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s')

handler.setFormatter(formatter)

logger.addHandler(handler)

logger.info(msg="Test the custom Logger")

#logger.propagate = False



