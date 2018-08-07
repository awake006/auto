import json
import sys
from urllib.parse import urljoin

from auto import global_data
from auto.log import console_logger
from auto.request import request
from auto.response import chenk


def _get_case_data(testcase_id):
    name = global_data.testcase[testcase_id].get("name")
    method = global_data.testcase[testcase_id].get("method", "GET").upper()
    message = global_data.testcase[testcase_id].get('message', 'success')
    request_type = global_data.testcase[testcase_id].get("type")
    chenk_method = global_data.testcase[testcase_id].get('chenk_method', 'message').upper()
    url = global_data.testcase[testcase_id].get('url')
    return name, method, message, request_type, chenk_method, url


def run(testcase_id):
    if not global_data.testcase.has_keys(testcase_id):
        case_not_exist = 'Test case [%s] does not exist' % testcase_id
        console_logger.info(case_not_exist)
        sys.exit()
    name, method, message, request_type, chenk_method, url = _get_case_data(testcase_id)
    url = urljoin(global_data.host, url)
    message_info_case = 'RUN CASE[%s]--NAME[%s]--[%s]--[%s]' % (testcase_id, name, method, url)
    console_logger.info(message_info_case)
    testcase_response = request(request_type, testcase_id, method, url)
    if isinstance(testcase_response, int):
        try:
            assert testcase_response is str
        except AssertionError as e:
            raise_message = 'The use case [%s] failed to execute, the use case [%s] parameter could not be built, and the use case was not executed yet.%s' % (
                testcase_response, testcase_id, e)
            console_logger.warning(raise_message)
            raise raise_message
    try:
        testcase_response = testcase_response.json()
        result = chenk(testcase_id, testcase_response, chenk_method, message)
    except json.JSONDecodeError as e:
        raise e
    try:
        assert result is True
    except AssertionError as e:
        raise_message = 'Test case [%s] execution failed.%s' % (
            testcase_id, e)
        console_logger.error(raise_message)
        raise raise_message
    if method == 'DELETE':
        global_data.testcase_result.pop(global_data.testcase_id.get(testcase_id))
    else:
        global_data.testcase_result[testcase_id] = testcase_response.get('data')
    return True
