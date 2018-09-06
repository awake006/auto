import json
import sys
from urllib.parse import urljoin

import requests

from auto import exception, global_data, operate_data
from auto.connet_mysql import SelectMySQL
from auto.exception import ParameterFormatException
from auto.global_data import DB
from auto.log import console_logger
from auto.operate_data import get_case_data


def run(testcase_id):
    if testcase_id not in global_data.testcase:
        case_not_exist = 'Test case [%s] does not exist' % testcase_id
        console_logger.info(case_not_exist)
        sys.exit()
    name, _, method, message, request_type, check_method, url = get_case_data(testcase_id)
    url = urljoin(global_data.host, url)
    message_info_case = 'RUN CASE[%s]--NAME[%s]--[%s]--[%s]' % (testcase_id, name, method, url)
    console_logger.info(message_info_case)
    testcase_response = Request(request_type, testcase_id, method, url).request()
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


class Request(object):
    def __init__(self, request_type, testcase_id, method, url):
        self.request_type = request_type
        self.testcase_id = testcase_id
        self.method = method
        self.url = url

    def request(self):
        '''Execute an http request and return the result'''
        requests_dict = {
            'POST': lambda: self._post(),
            'GET': lambda: self._put(),
            'DELETE': lambda: self._delete(),
            'PUT': lambda: self._put()
        }
        return requests_dict[self.method]()

    def _post(self):
        if self.request_type:
            files = format_file_parameter(self.testcase_id)
            response = requests.post(headers=global_data.headers, url=self.url, files=files)
        else:
            data = format_parameter(self.testcase_id)
            response = requests.post(headers=global_data.headers, url=self.url, json=data)
        return response

    def _get(self):
        data = format_parameter(self.testcase_id)
        response = requests.get(headers=global_data.headers, url=self.url, params=data)
        return response

    def _put(self):
        url, data = format_put_delete(self.url, self.testcase_id)
        response = requests.put(headers=global_data.headers, url=url, json=data)
        return response

    def _delete(self):
        url, data = format_put_delete(self.url, self.testcase_id)
        response = requests.delete(headers=global_data.headers, url=url, json=data)
        return response


def check(testcase_id, response, check_method, message):
    checks = {
        'MESSAGE': lambda: _check_message(response, message),
        'DB': lambda: _check_db(testcase_id),
        'STATUS': lambda: _check_status(200),

    }
    return checks[check_method]()


def _check_message(response, message):
    '''
    Get test results for a use case
    '''
    result_message = response.get("msg")
    if result_message == message:
        return True
    else:
        return False


def _check_db(testcase_id):
    sql = global_data.testcase[testcase_id].get('sql')
    if '%' in sql:
        for value in global_data.testcase_parameter.get(testcase_id).values():
            if isinstance(value, list):
                continue
            param_value = value
            break
        sql = sql % param_value
    db = SelectMySQL(DB.host, DB.username, DB.password, DB.db)
    db.connect()
    sql_result = db.select_one(sql)
    data = global_data.testcase_parameter.get(testcase_id)
    for key in data.keys():
        if data[key] == sql_result[key]:
            continue
        else:
            return False
    return True


def _check_status(status):
    pass


def format_file_parameter(testcase_id):
    data = {}
    try:
        parameter = global_data.testcase.get(testcase_id)['parameter']
        data = _format_file(parameter, testcase_id)
        global_data.testcase_parameter[testcase_id] = data
        return data
    except (KeyError, FileNotFoundError) as e:
        message_error_format_param = 'The use case [%s] parameter setting is incorrect, please check the parameter file [%s]' % (
            testcase_id, e)
        console_logger.error(message_error_format_param)
        raise e


def format_parameter(testcase_id):
    data = {}
    parameter = global_data.testcase.get(testcase_id).get('parameter')
    if parameter:
        data = _format_param(parameter, testcase_id)
        global_data.testcase_parameter[testcase_id] = data
    return data


def format_put_delete(url, testcase_id):
    data = {}
    try:
        parameter = global_data.testcase.get(testcase_id)['parameter']
        for key in parameter:
            if isinstance(parameter.get(key), dict):
                """
                Dictionary, need to get data from other interfaces
                """
                testcase_dict = parameter.get(key)
                old_case_id = testcase_dict.get('id')
                global_data.testcase_id[testcase_id] = old_case_id
                testcase_result = global_data.testcase_result.get(old_case_id)
                if not testcase_result:
                    run(old_case_id)
                    testcase_result = global_data.testcase_result.get(old_case_id)
                    if not testcase_result:
                        parameter_format_error = '''The use case {} failed to execute,
                        the use case {} parameter could not be built,
                        and the use case was not executed yet.'''.format(old_case_id, testcase_id)
                        console_logger.error(parameter_format_error)
                        raise ParameterFormatException(parameter_format_error)
                if isinstance(testcase_result, list):
                    testcase_result = testcase_result[0]
                new_url = url % testcase_result.get(testcase_dict.get('value'))
            elif str(parameter.get(key)).split(',')[0] == 'str':
                data[key] = operate_data.set_str(parameter.get(key).split(',')[1], testcase_id)
            elif parameter.get(key) == "random":
                data[key] = operate_data.set_time()
            else:
                data[key] = parameter.get(key)
        global_data.testcase_parameter[testcase_id] = data
        return new_url, data
    except (KeyError, FileNotFoundError) as e:
        message_error_format_param = 'The use case [%s] parameter setting is incorrect, please check the parameter file [%s]' % (
            testcase_id, e)
        console_logger.error(message_error_format_param)
        raise e


def _format_param(parameter, testcase_id):
    data = {}
    if not isinstance(parameter, dict):
        raise ParameterFormatException('testcase-{} parameter format fail')
    for key in parameter:
        if isinstance(parameter.get(key), dict):
            """
            Dictionary, need to get data from other interfaces
            """
            testcase_dict = parameter.get(key)
            old_case_id = testcase_dict.get('id')
            global_data.testcase_id[testcase_id] = old_case_id
            testcase_result = global_data.testcase_result.get(old_case_id)
            if not testcase_result:
                run(old_case_id)
                testcase_result = global_data.testcase_result.get(old_case_id)
                if not testcase_result:
                    parameter_format_error = '''The use case {} failed to execute,
                     the use case {} parameter could not be built,
                     and the use case was not executed yet.'''.format(old_case_id, testcase_id)
                    console_logger.error(parameter_format_error)
                    raise ParameterFormatException(parameter_format_error)
            if isinstance(testcase_result, list):
                testcase_result = testcase_result[0]
            data[key] = testcase_result.get(testcase_dict.get('value'))
        elif isinstance(parameter.get(key), list):
            data_list = []
            for p in parameter.get(key):
                p_data = _format_param(p, testcase_id)
                data_list.append(p_data)
            data[key] = data_list
        elif str(parameter.get(key)).split(',')[0] == 'str':
            data[key] = operate_data.set_str(parameter.get(key).split(',')[1], testcase_id)

        elif parameter.get(key) == "random":
            data[key] = operate_data.set_time()
        else:
            data[key] = parameter.get(key)
    return data


def _format_file(parameter, testcase_id):
    data = {}
    for key in parameter:
        if isinstance(parameter.get(key), dict):
            """
            Dictionary, need to get data from other interfaces
            """
            testcase_dict = parameter.get(key)
            old_case_id = testcase_dict.get('id')
            global_data.testcase_id[testcase_id] = old_case_id
            testcase_result = global_data.testcase_result.get(old_case_id)
            if not testcase_result:
                run(old_case_id)
                testcase_result = global_data.testcase_result.get(old_case_id)
                if not testcase_result:
                    parameter_format_error = '''The use case {} failed to execute,
                     the use case {} parameter could not be built,
                     and the use case was not executed yet.'''.format(old_case_id, testcase_id)
                    console_logger.error(parameter_format_error)
                    raise ParameterFormatException(parameter_format_error)
            if isinstance(testcase_result, list):
                testcase_result = testcase_result[0]
            data[key] = (None, str(testcase_result.get(testcase_dict.get('value'))))
        elif str(parameter.get(key)).split(',')[0] == 'str':
            data[key] = (None, operate_data.set_str(parameter.get(key).split(',')[1], testcase_id))
        elif parameter.get(key) == "random":
            data[key] = (None, str(operate_data.set_time()))

        elif key == "video":
            data[key] = ("video.mp4", open(
                parameter.get(key), 'rb'), "video/mp4")
        elif key == "img":
            data[key] = ('img.png', open(
                parameter.get(key), 'rb'), "image/jpg/png/jpeg")
        else:
            data[key] = (None, str(parameter.get(key)))
    return data
