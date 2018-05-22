import os

from common.count_case import CountResult
from common.get_case import import_case
from common.operate_file import operate_yaml
from common.report_excel import ReportExcel
from common.new_run_case import StartTest
# from common.send_email import send_email

def start(base):
    '''
    测试主函数入口
    '''
    test = StartTest(base)
    for index in test.number:
        if index:
            print("正在执行用例:%s...." % index)
            case_result, is_pass = test.run_case(index)
            CountResult.total += 1
            if is_pass:
                case_result.append("pass")
                CountResult.success += 1
            else:
                case_result.append("fail")
                CountResult.fail += 1
            test.results.append(case_result)
        else:
            continue
    return test.results


def PATH(p): return os.path.abspath(p)


if __name__ == "__main__":
    path = os.getcwd()
    case_path = PATH(os.path.join(path, 'case/case_yaml'))
    import_case(case_path)
    base_info_path = PATH(os.path.join(path, 'config/base_info.yaml'))
    base_info = operate_yaml(base_info_path)[0]
    result = start(base_info)
    report_path = PATH(os.path.join(path, 'reports'))
    excel = ReportExcel(result, report_path)
    excel.set_excel()
    print("执行完毕....")