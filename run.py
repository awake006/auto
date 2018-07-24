import os
import sys
from api.data import Count
from api.operate_file import operate_yaml, import_case, set_excel
from api.runner import RunTest
from optparse import OptionParser
from api.log import console_logger, setup_logging
from api.data import Case
import logging
# from common.send_email import send_email


def log_init(path_p):
    path = os.path.abspath(path_p)
    f = open(path, 'w')
    f.close()
    setup_logging(loglevel='info', logfile=path)
    logger = logging.getLogger(__name__)


def parse_options():
    parser = OptionParser('Api Test')
    parser.add_option(
        '-C', '--case',
        dest='case',
        default=None,
        # action="store_false",
        help='Run test case list,between case "," default get from config file'
    )
    parser.add_option(
        '-H', '--host',
        dest='host',
        default=None,
        help='Run case host,default get from config file'
    )
    opts, _ = parser.parse_args()
    return opts


def PATH(p):
    return os.path.abspath(p)


def main():
    '''
    测试主函数入口
    '''
    opts = parse_options()
    # if opts.host:
    host = opts.host
    case_no = opts.case
    path = os.getcwd()
    case_path = PATH(os.path.join(path, 'case/case_yaml'))
    import_case(case_path)
    base_info_path = PATH(os.path.join(path, 'config/base_info.yaml'))
    config_data = operate_yaml(base_info_path)[0]
    test = RunTest(config_data, host, case_no)
    test_result = []
    for index in test.case_no:
        if index:
            console_logger.info("正在执行用例:%s...." % index)
            case_result, is_pass = test.run_case(index)
            Count.total += 1
            if is_pass:
                case_result.append("pass")
                Count.success += 1
            else:
                case_result.append("fail")
                Count.fail += 1
            test_result.append(case_result)
        else:
            continue
    report_path = PATH(os.path.join(path, 'reports'))
    excel = set_excel(test_result, report_path)
    console_logger.info('执行完毕')


if __name__ == "__main__":
    main()
