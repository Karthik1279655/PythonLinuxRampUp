import logging

logging.basicConfig(filename="report.txt",
                    filemode='a',
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

for i in range(0, 10):
    if i % 2 == 0:
        logging.warning('Log Warning Message')

    elif i % 3 == 0:
        logging.info('Log Info Message')

    else:
        logging.error('Log Error Message')

