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
    return logger


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
    parser.add_option(
        '-P', '--case-path',
        dest='case_dir',
        default=None,
        help='Case dir abspath,default cmd-dir case/case_yaml'
    )
    parser.add_option(
        '-G', '--config-file',
        dest='config_file',
        default=None,
        help='Config file abspath,default default cmd-dir config/base_info.yaml'
    )
    opts, _ = parser.parse_args()
    return opts


def PATH(p):
    return os.path.abspath(p)


def main():
    '''
    测试主函数入口
    '''
    # 读取命令行参数
    opts = parse_options()
    host = opts.host
    case_no = opts.case
    case_dir = opts.case_dir
    config_file = opts.config_file
    # 日志文件配置
    path = os.getcwd()
    log_dir = os.path.join(path, 'log')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    log_path = os.path.join(log_dir, 'test.log')
    logger = log_init(log_path)
    # 用例、配置导入
    if not case_dir:
        case_dir = PATH(os.path.join(path, 'case/case_yaml'))
    import_case(case_dir)
    if not config_file:
        config_file = PATH(os.path.join(path, 'config/base_info.yaml'))
    config_data = operate_yaml(config_file)[0]

    # 初始化测试
    test = RunTest(config_data, host, case_no, logger)
    test_result = []
    # 执行测试
    for index in sorted(test.case_no):
        message_info = "正在执行用例:%s...." % index
        console_logger.info(message_info)
        case_result, is_pass = test.run_case(index)
        Count.total += 1
        if is_pass:
            message_info_case = '用例[%s]执行成功' % index
            case_result.append("pass")
            Count.success += 1
        else:
            message_info_case = '用例[%s]执行失败' % index
            case_result.append("fail")
            Count.fail += 1
        console_logger.info(message_info_case)
        test_result.append(case_result)
    # 生成测试报告
    if not os.path.exists(os.path.join(path, 'reports')):
        os.mkdir(os.path.join(path, 'reports'))
    report_path = PATH(os.path.join(path, 'reports'))
    excel = set_excel(test_result, report_path)
    message_info_excel = '执行完毕,通过[%s]查看测试结果' % excel
    console_logger.info(message_info_excel)


if __name__ == "__main__":
    main()
