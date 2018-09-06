import json
import sys
from urllib.parse import urljoin

from auto import global_data
from auto.log import console_logger
from auto.request import request
from auto.response import check
from auto.build_data import get_case_data
from auto import exception


def run(testcase_id):
    if testcase_id not in global_data.testcase:
        case_not_exist = 'Test case [%s] does not exist' % testcase_id
        console_logger.info(case_not_exist)
        print(global_data.testcase)
        sys.exit()
    name, _, method, message, request_type, check_method, url = get_case_data(testcase_id)
    url = urljoin(global_data.host, url)
    message_info_case = 'RUN CASE[%s]--NAME[%s]--[%s]--[%s]' % (testcase_id, name, method, url)
    console_logger.info(message_info_case)
    testcase_response = request(request_type, testcase_id, method, url)
    if isinstance(testcase_response, int):
        raise exception.ParameterBuildFailedException(
            'The use case [%s] failed to execute, the use case [%s] parameter could not be built, and the use case was not executed yet.' % (testcase_response, testcase_id))
    testcase_response.encoding = 'utf-8'
    try:
        testcase_response_json = testcase_response.json()
    except json.JSONDecodeError:
        raise exception.ReturnFormatException(testcase_response.text)

    result = check(testcase_id, testcase_response_json, check_method, message)
    if not result:
        raise exception.CaseFailException('case fail')
    if method == 'DELETE':
        global_data.testcase_result.pop(global_data.testcase_id.get(testcase_id))
    else:
        global_data.testcase_result[testcase_id] = testcase_response_json.get('data')
    return True
