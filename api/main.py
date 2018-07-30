import logging
import os
import sys
import time
from optparse import OptionParser

from api.create_example import create
from api.data import Case, Count
from api.log import console_logger, setup_logging
from api.operate_file import import_case, operate_yaml, set_excel
from api.runner import RunTest

# from common.send_email import send_email


def log_init(path_p):
    path = os.path.abspath(path_p)
    f = open(path, 'w')
    f.close()
    setup_logging(loglevel='info', logfile=path)
    logger = logging.getLogger(__name__)
    return logger


def parse_options():
    parser = OptionParser('Api Test')
    parser.add_option(
        '-C', '--case',
        dest='case',
        default=None,
        # action="store_false",
        help='Run a list of test cases, separated by ",", read from the configuration file by default'
    )
    parser.add_option(
        '-H', '--host',
        dest='host',
        default=None,
        help='Run the test host, read from the configuration file by default'
    )
    parser.add_option(
        '-P', '--case-path',
        dest='case_dir',
        default=None,
        help='Test case folder absolute path, default case folder under the execution folder'
    )
    parser.add_option(
        '-G', '--config-file',
        dest='config_file',
        default=None,
        help='The absolute path of the configuration file, the config/base_info.yaml file under the default execution folder'
    )
    parser.add_option(
        '-T', '--create-templete',
        dest='create_templete',
        default=None,
        help='Create test cases and configuration file templates, stored in the api folder under the execution folder'
    )
    opts, _ = parser.parse_args()
    return opts


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
    is_create = opts.create_templete

    path = os.getcwd()

    if is_create:
        create(path)
        print("Create template successfully")
        sys.exit()
    # Log file configuration
    log_dir = os.path.join(path, 'log')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    log_filename = str(time.strftime("%Y%m%d%H%M%S", time.localtime())) + '.log'
    log_path = os.path.join(log_dir, log_filename)
    logger = log_init(log_path)
    # Use case, configuration import
    if not case_dir:
        case_dir = PATH(os.path.join(path, 'case'))
    import_case(case_dir)
    if not config_file:
        config_file = PATH(os.path.join(path, 'config/base_info.yaml'))
    config_data = operate_yaml(config_file)[0]

    # Initialization test
    test = RunTest(config_data, host, case_no, logger)
    test_result = []
    # Execution test
    for index in sorted(test.case_no):
        message_info = "Executing use case[%s]...." % index
        console_logger.info(message_info)
        case_result, is_pass = test.run_case(index)
        Count.total += 1
        if is_pass:
            message_info_case = 'Use case [%s] executed successfully' % index
            case_result.append("pass")
            Count.success += 1
        else:
            message_info_case = 'Use case [%s] failed to execute' % index
            case_result.append("fail")
            Count.fail += 1
        console_logger.info(message_info_case)
        test_result.append(case_result)
    # Generate test report
    if not os.path.exists(os.path.join(path, 'reports')):
        os.mkdir(os.path.join(path, 'reports'))
    report_path = PATH(os.path.join(path, 'reports'))
    excel = set_excel(test_result, report_path)
    message_info_excel = 'Execution is complete, check the test results with [%s]' % excel
    console_logger.info(message_info_excel)


if __name__ == "__main__":
    main()
