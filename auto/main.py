import logging
import os
import sys
import time
import unittest
from xmlrunner import XMLTestRunner

from auto import global_data
from auto.cli_param import parse_options
from auto.create import *
from auto.log import setup_logging, console_logger
from auto.operate_file import *
from auto.runhtml import HTMLTestRunner


def log_init(path_p):
    path = os.path.abspath(path_p)
    f = open(path, 'w')
    f.close()
    setup_logging(loglevel='info', logfile=path)
    logger = logging.getLogger(__name__)
    return logger


def PATH(p):
    return os.path.abspath(p)


def loading_data(testcase_dir, config_file, token):
    conversion_case(testcase_dir)
    config_data = operate_yaml(config_file)[0]
    global_data.host = config_data.get('host')
    global_data.headers = config_data.get('headers')
    global_data.token = config_data.get('token')
    if token:
        global_data.token = token
    global_data.DB.db = config_data.get('db')
    global_data.DB.host = config_data.get('db_host')
    global_data.DB.username = config_data.get('db_username')
    global_data.DB.password = config_data.get('db_password')
    testcase_id_list = config_data.get('case_id_list')
    return testcase_id_list


def main():
    '''
    Test main function entry
    '''
    # Read command line arguments
    opts = parse_options()
    host = opts.host
    is_create = opts.create_template
    report_format = opts.format
    token = opts.token
    path = os.getcwd()

    if is_create:
        create_example(path)
        print("Create template successfully")
        sys.exit()
    # Log file configuration
    log_dir = PATH(os.path.join(path, 'log'))
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    log_filename = str(time.strftime("%Y%m%d%H%M%S", time.localtime())) + '.log'
    log_path = PATH(os.path.join(log_dir, log_filename))
    log_init(PATH(log_path))
    # Use case, configuration import
    case_dir = PATH(os.path.join(path, 'case/yaml'))
    config_file = PATH(os.path.join(path, 'config/config.yaml'))
    if host and (host == 'test'):
        config_file = PATH(os.path.join(path, 'config/test_config.yaml'))
    testcase_id_list = loading_data(case_dir, config_file, token)
    script_dir = PATH(os.path.join(path, 'case/script'))
    script_file = PATH(os.path.join(script_dir, 'test_allcase.py'))
    create_script(script_file, testcase_id_list)
    # Generate test report
    suit = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(script_dir, pattern='test_*')
    for i in discover:
        suit.addTest(i)
    runner = HTMLTestRunner(output='reports')
    if report_format and (report_format == 'xml' or report_format == 'XML'):
        runner = XMLTestRunner(output='reports')
    runner.run(suit)


if __name__ == "__main__":
    main()
