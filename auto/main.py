from auto.log import setup_logging, console_logger
import logging
import os
from auto.cli_param import parse_options
import time
import sys
from auto.operate_file import conversion_case, operate_yaml
from auto.create import create_example


def log_init(path_p):
    path = os.path.abspath(path_p)
    f = open(path, 'w')
    f.close()
    setup_logging(loglevel='info', logfile=path)
    logger = logging.getLogger(__name__)
    return logger


def PATH(p):
    return os.path.abspath(p)


def main():
    '''
    Test main function entry
    '''
    # Read command line arguments
    opts = parse_options()
    host = opts.host
    case_no = opts.case
    case_dir = opts.case_dir
    config_file = opts.config_file
    is_create = opts.create_template

    path = os.getcwd()

    if is_create:
        create_example(path)
        print("Create template successfully")
        sys.exit()
    # Log file configuration
    log_dir = os.path.join(path, 'log')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    log_filename = str(time.strftime("%Y%m%d%H%M%S", time.localtime())) + '.log'
    log_path = os.path.join(log_dir, log_filename)
    log_init(PATH(log_path))
    # Use case, configuration import
    if not case_dir:
        case_dir = PATH(os.path.join(path, 'case/yaml'))
    conversion_case(case_dir)
    if not config_file:
        config_file = PATH(os.path.join(path, 'config/config.yaml'))
    config_data = operate_yaml(config_file)[0]

    # Initialization test

    # Generate test report
    if not os.path.exists(os.path.join(path, 'reports')):
        os.mkdir(os.path.join(path, 'reports'))
    report_path = PATH(os.path.join(path, 'reports'))


if __name__ == "__main__":
    main()
