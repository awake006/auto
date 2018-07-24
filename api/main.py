import logging
import os
from optparse import OptionParser

from api.log import console_logger, setup_logging


def log_test(path_p):
    path = os.path.abspath(path_p)
    f = open(path, 'w')
    f.close()
    setup_logging(loglevel='info', logfile=path)
    logger = logging.getLogger(__name__)
    logger.error('error')
    logger.info('info')
    logger.warning('warning')
    console_logger.info('console info')


def parse_options():
    parser = OptionParser(usage="test")
    parser.add_option(
        '-n',
        dest='number',
        type='int',
        help='input number'
    )
    opts, _ = parser.parse_args()
    return opts


def main():
    master_path = os.getcwd()
    path = os.path.join(master_path, 'test.log')
    log_test(path)
    value_obj = parse_options()
    if value_obj.number:
        console_logger.info(value_obj.number)
        console_logger.warning('number is None')
    else:
        console_logger.error('please input number,use -n value')


if __name__ == '__main__':
    main()
