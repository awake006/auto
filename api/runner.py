import json
import random
import string
import sys
import time
from urllib.parse import urljoin

import requests

from api.connet_mysql import SelectMySQL
from api.data import ApiParam, Case, CaseResult
from api.log import console_logger


class RunTest(object):
    def __init__(self, config_data, host, case_no, logger):
        if host:
            self.host = host
        else:
            self.host = config_data.get('host')
        if case_no:
            case_ = case_no.split(',')
        else:
            if config_data.get("case_no"):
                case_ = config_data.get("case_no").split(',')
            else:
                case_ = _get_case_no()
        self.case_no = [i for i in case_ if i != '']
        self.logger = logger
        self.headers = config_data.get('headers')
        self.db = config_data.get('db')
        self.db_username = config_data.get("db_username")
        self.db_password = config_data.get('db_password')
        self.db_host = config_data.get("db_host")
        self.login_url = config_data.get('login_url')
        self.login_username = config_data.get("login_username")
        self.login_password = config_data.get("login_password")

    def _sign_in(self):
        '''
        login
        '''
        url = urljoin(self.host, self.login_url)
        data = {'account': self.login_username, 'password': str(self.login_password)}
        json_data = json.dumps(data)
        response = requests.post(url=url, headers=self.headers, json=data)
        if response.status_code != 200:
            message_error_login = 'Login failed, please reconfigure login parameters%s,%s' % (json_data, url)
            console_logger.error(message_error_login)
            sys.exit()
        return response.headers['token']

    def _format_file_param(self, index):
        '''
        Format file upload parameters
        '''
        data = {}
        try:
            params = Case.case.get(index)['params']
            for key in params:
                if isinstance(params.get(key), dict):
                    """
                    Dictionary, need to get data from other interfaces
                    """
                    case_dict = params.get(key)
                    case_id = case_dict.get('id')
                    case_data = CaseResult.case_result.get(case_id)
                    if case_data:
                        case_result = case_data
                    else:
                        self.run_case(case_id)
                        case_result = CaseResult.case_result.get(case_id)

                        if case_result:
                            if type(case_result) != list:
                                v = case_result
                            else:
                                v = case_result[0]
                            data[key] = (None, str(v.get(case_dict.get('value'))))
                        else:
                            return int(case_id)

                elif str(params.get(key)).split(',')[0] == 'str':
                    data[key] = _set_str(params.get(key).split(',')[1], index)

                elif params.get(key) == "random":
                    data[key] = (None, str(_set_time()))

                elif key == "video":  # 上传MP4格式的文件
                    data[key] = ("video.mp4", open(
                        params.get(key), 'rb'), "video/mp4")

                elif key == "img":  # 上传类型是图片
                    data[key] = ('img.png', open(
                        params.get(key), 'rb'), "image/jpg/png/jpeg")
                else:
                    data[key] = (None, str(params.get(key)))

            ApiParam.param[index] = data
            return data
        except (KeyError, FileNotFoundError) as e:
            message_error_format_param = 'The use case [%s] parameter setting is incorrect, please check the parameter file [%s]' % (index, e)
            console_logger.error(message_error_format_param)
            sys.exit()

    def _format_param(self, index):
        '''
        Formatting parameters
        '''
        data = {}
        try:
            params = Case.case.get(index)['params']
            for key in params:
                if isinstance(params.get(key), dict):
                    """
                    Dictionary, need to get data from other interfaces
                    """
                    case_dict = params.get(key)
                    case_id = case_dict.get('id')
                    case_data = CaseResult.case_result.get(case_id)
                    if case_data:
                        case_result = case_data
                    else:
                        self.run_case(case_id)
                        case_result = CaseResult.case_result.get(case_id)

                        if case_result:
                            if type(case_result) != list:
                                v = case_result
                            else:
                                v = case_result[0]

                            data[key] = v.get(case_dict.get('value'))
                        else:
                            return int(case_id)

                elif str(params.get(key)).split(',')[0] == 'str':
                    data[key] = _set_str(params.get(key).split(',')[1], index)

                elif params.get(key) == "random":
                    data[key] = _set_time()

                else:
                    data[key] = params.get(key)

            ApiParam.param[index] = data
            return data
        except KeyError as e:
            message_error_format_param = 'The use case [%s] parameter setting is incorrect, please check the parameter file [%s]' % (index, e)
            console_logger.error(message_error_format_param)
            sys.exit()

    def _format_put_or_delete(self, url, index):
        data = {}
        return url, data

    def requests_case(self, request_type, index, method, urls):
        '''Execute an http request and return the result'''
        requests_dict = {
            'POST': lambda: self._post(request_type, index, urls),
            'GET': lambda: self._put(index, urls),
            'DELETE': lambda: self._delete(index, urls),
            'PUT': lambda: self._put(index, urls)
        }
        return requests_dict[method]()

    def _post(self, request_type, index, urls):
        if request_type:
            files = self._format_file_param(index)
            if isinstance(files, dict):
                response = requests.post(headers=self.headers, url=urls, files=files)
            else:
                response = files
        else:
            data = self._format_param(index)
            if isinstance(data, dict):
                response = requests.post(headers=self.headers, url=urls, json=data)
            else:
                response = data
        return response

    def _get(self, index, urls):
        data = self._format_param(index)
        if isinstance(data, dict):
            response = requests.get(headers=self.headers, url=urls, params=data)
        else:
            response = data
        return response

    def _put(self, index, urls):
        urls, data = self._format_put_or_delete(urls, index)
        if isinstance(data, dict):
            response = requests.put(headers=self.headers, url=urls, json=data)
        else:
            response = data
        return response

    def _delete(self, index, urls):
        urls, data = self._format_put_or_delete(urls, index)
        if isinstance(data, dict):
            response = requests.delete(headers=self.headers, url=urls, json=data)
        else:
            response = data
        return response

    def chenk(self, index, result, result_value, chenk_method, message):
        chenks = {
            'MESSAGE': lambda: self._chenk_message(result, result_value, message),
            'DB': lambda: self._chenk_db(index, result),
            'STATUS': lambda: self._chenk_status(200),

        }
        return chenks[chenk_method]()

    def _chenk_message(self, result, result_value, message):
        '''
        Get test results for a use case
        '''
        result.append(message)
        result_message = result_value.get("msg")
        result.append(result_message)
        if result_message == message:
            return True
        else:
            return False

    def _chenk_db(self, index, result):
        sql = Case.case[index].get('sql')
        if '%' in sql:
            for value in ApiParam.param.get(index).values():
                if isinstance(value, list):
                    continue
                param_value = value
                break
            sql = sql % param_value
        db = SelectMySQL(self.db_host, self.db_username, self.db_password, self.db)
        db.connect()
        sql_result = db.select_one(sql)
        data = ApiParam.param.get(index)
        result.append(str(data))
        result.append(str(sql_result))
        for key in data.keys():
            if data[key] == sql_result[key]:
                continue
            else:
                return False
        return True

    def _chenk_status(self, status):
        pass

    def run_case(self, index):
        '''
        Run a request
        '''
        if index not in Case.case:
            message_error_not_in_case = 'Use case [%s] does not exist' % index
            console_logger.error(message_error_not_in_case)
            sys.exit()
        index = int(index)
        is_login = Case.case[index].get('login')
        if is_login:
            self.headers['token'] = self._sign_in()
        result = []
        result_value = {}
        try:
            name, method, message, request_type, chenk_method, url = _get_case_data(index, result)
        except KeyError as e:
            message_error_param = 'The use case [%s] parameter setting is incorrect, please check the parameter file [%s]' % (index, e)
            console_logger.error(message_error_param)
            sys.exit()
        urls = urljoin(self.host, url)
        message_info_case = 'RUN CASE[%s]--NAME[%s]--[%s]--[%s]' % (index, name, method, urls)
        console_logger.info(message_info_case)
        response = self.requests_case(request_type, index, method, urls)
        if not isinstance(response, int):
            try:
                result_value = response.json()
                is_pass = self.chenk(index, result, result_value, chenk_method, message)
            except json.JSONDecodeError as e:
                result.append('The result is not in json format')
                result.append('status_code:%s' % response.status_code)
                is_pass = False
        else:
            result.append('Use case [%s] failed to execute' % response)
            result.append('')
            message_warning_case = 'The use case [%s] failed to execute, the use case [%s] parameter could not be built, and the use case was not executed yet.' % (
                response, index)
            self.logger.warning(message_warning_case)
            console_logger.warning(message_warning_case)
            is_pass = False
        if is_pass:
            CaseResult.case_result[index] = result_value.get('data')
        return result, is_pass


def _get_case_data(index, result):
    name = Case.case[index].get("name")
    method = Case.case[index].get("method", "GET").upper()  # 默认为get请求
    message = Case.case[index].get('message', 'success')
    request_type = Case.case[index].get("type")
    # 校验方式，默认message为数据，另外包括db校验，status校验,page
    chenk_method = Case.case[index].get('chenk_method', 'message').upper()
    url = Case.case[index].get('url')
    result.append(index)
    result.append(name)
    result.append(url)
    result.append(method)
    return name, method, message, request_type, chenk_method, url


def _set_str(n, index):
    '''
    Randomly generate n-bit str
    '''
    try:
        n = int(n)
        source = list(string.ascii_letters) + list(string.digits)
        name = ''
        for _ in range(n):
            name += random.choice(source)
        return name
    except TypeError as e:
        console_logger.error('The use case [%s] parameter setting is incorrect, please check the parameter file [%s]' % (index, e))
        sys.exit()


def _set_time():
    '''strftime'''
    now_time = time.strftime("%Y%m%d%H%M%s", time.localtime())
    return now_time


def _get_case_no():
    case_no = [i for i in Case.case.keys() if i != '']
    return case_no
