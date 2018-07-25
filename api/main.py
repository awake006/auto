import os
import time
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
        help='Case dir abspath,default cmd-dir case'
    )
    parser.add_option(
        '-G', '--config-file',
        dest='config_file',
        default=None,
        help='Config file abspath,default default cmd-dir config/base_info.yaml'
    )
    parser.add_option(
        '-T', '--create-templete',
        dest='create_templete',
        default=None,
        help='Create templete'
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
    is_create = opts.create_templete
    if is_create:
        create()
        print("创建模板成功")
        sys.exit()
    # 日志文件配置
    path = os.getcwd()
    log_dir = os.path.join(path, 'log')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    log_filename = str(time.strftime("%Y%m%d%H%M%S", time.localtime())) + '.log'
    log_path = os.path.join(log_dir, log_filename)
    logger = log_init(log_path)
    # 用例、配置导入
    if not case_dir:
        case_dir = PATH(os.path.join(path, 'case'))
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


def create():
    path = os.getcwd()
    base_dir = os.path.join(path, 'api')
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    case_dir = os.path.join(base_dir, 'case')
    if not os.path.exists(case_dir):
        os.mkdir(case_dir)
    config_dir = os.path.join(base_dir, 'config')
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)
    case_templete = os.path.abspath(os.path.join(case_dir, 'case_templete.yaml'))
    config_templete = os.path.abspath(os.path.join(config_dir, 'config_templete.yaml'))
    with open(case_templete, 'w', encoding='utf-8') as f:
        case_str = r'''
- name: 加入比赛
  method: POST
  type: file
  hope: $sucess
  url: api/work/store
  id: 1003
  params:
    user_id: 3
    contest_id:
      id: 1004
      value: contest_id
    group_id:
      id: 1002
      value: group_id
    longitude: '113.9401565012'
    latitude: '22.5496157178'
    address: shenzhen
- name: 创建比赛
  method: POST
  type: file
  hope: sucess
  url: api/contest/store
  id: 1004
  params:
    user_id: 3
    group_id:
      id: 1002
      value: group_id
    video: D:\video\20s.mp4
    img: G:\picture\link.jpg
    longitude: '113.9401565012'
    latitude: '22.5496157178'
    address: shenzhen
    description: name
    title: random
    video_time: 20
        '''
        f.write(case_str)
    with open(config_templete, 'w', encoding='utf-8')as f:
        config_str = r'''
- title: 
  case_no: 
  host:
  db_username: 
  db_password: 
  db_host: 
  db: 
  login_url: 
  login_username: 
  login_password: 
  headers:
    Accept-Encoding: gzip;q=1.0,compress;q=0.5
    Accept-Language: zh-Hans-CN;q=1.0,en-CN;q=0.9,zh-Hant-CN;q=0.8
    User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36
        '''
        f.write(config_str)


if __name__ == "__main__":
    # main()
    create()
