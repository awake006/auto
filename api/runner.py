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
    def __init__(self, config_data, host, case_no):
        if host:
            self.host = host
        else:
            self.host = config_data.get('host')
        if case_no:
            self.case_no = case_no
        else:
            if config_data.get("case_no"):
                self.case_no = config_data.get("case_no").split(',')
            else:
                self.case_no = self._get_case_no()

        self.headers = config_data.get('headers')
        self.db = config_data.get('db')
        self.db_username = config_data.get("db_username")
        self.db_password = config_data.get('db_password')
        self.db_host = config_data.get("db_host")
        self.login_url = config_data.get('login_url')
        self.login_username = config_data.get("login_username")
        self.login_password = config_data.get("login_password")

    def _get_case_no(self):
        case_no = []
        for key in Case.case.keys():
            case_no.append(key)
        return case_no

    def _sign_in(self):
        '''
        获取用户登录token
        支持帐号登录可以写一个登录的方法
        '''
        url = urljoin(self.host, self.login_url)
        data = {'account': self.login_username, 'password': str(self.login_password)}
        json_data = json.dumps(data)
        response = requests.post(url=url, headers=self.headers, json=data)
        if response.status_code != 200:
            console_logger.error('登录失败，请重新配置登录参数%s,%s' % (json_data, url))
            sys.exit()
        return response.headers['token']

    def _set_str(self, n, index):
        '''
        随机生成n位的str
        '''
        try:
            n = int(n)
            source = list(string.ascii_letters) + list(string.digits)
            name = ''
            for _ in range(n):
                name += random.choice(source)
            return name
        except TypeError as e:
            console_logger.error('用例%s参数设置有误，请检查参数文件[%s]' % (index, e))
            sys.exit()

    def _set_time(self):
        '''时间，避免数据重复'''
        now_time = time.strftime("%Y%m%d%H%M%s", time.localtime())
        return now_time

    def _format_file_param(self, index):
        '''
        格式化文件上传的参数
        '''
        data = {}
        try:
            params = Case.case.get(index)['params']
        except KeyError as e:
            console_logger.error('用例%s参数设置有误，请检查参数文件[%s]' % (index, e))
            sys.exit()

        for key in params:
            if isinstance(params.get(key), dict):
                """
                字典，需要从别的接口获取数据
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
                        return case_id

            elif str(params.get(key)).split(',')[0] == 'str':
                data[key] = self._set_str(params.get(key).split(',')[1], index)

            elif params.get(key) == "random":
                data[key] = (None, str(self._set_time()))

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

    def _format_param(self, index):
        '''
        格式化获取参数
        '''
        data = {}
        try:
            params = Case.case.get(index)['params']
        except KeyError as e:
            console_logger.error('用例%s参数设置有误，请检查参数文件[%s]' % (index, e))
            sys.exit()

        for key in params:
            if isinstance(params.get(key), dict):
                """
                字典，需要从别的接口获取数据
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
                        return case_id

            elif str(params.get(key)).split(',')[0] == 'str':
                data[key] = self._set_str(params.get(key).split(',')[1], index)

            elif params.get(key) == "random":
                data[key] = self._set_time()

            else:
                data[key] = params.get(key)

        ApiParam.param[index] = data
        return data

    def _format_put_or_delete(self, url, index):
        data = {}
        return url, data

    def requests_case(self, request_type, index, method, urls):
        '''执行一次http请求，返回结果'''
        if request_type:
            files = self._format_file_param(index)
            if not isinstance(files, dict):
                request_data = json.dumps(files)
                response = requests.post(headers=self.headers, url=urls, files=files)
            else:
                return files

        else:
            if method == ("PUT" or "DELETE"):
                urls, data = self._format_put_or_delete(urls, index)
                if method == "PUT":
                    response = requests.post(headers=self.headers, url=urls, json=data)
                elif method == "DELETE":
                    response = requests.delete(headers=self.headers, url=urls, json=data)
            else:
                data = self._format_param(index)
                if not isinstance(data, dict):
                    return data
                request_data = json.dumps(data)
                if method == "POST":
                    response = requests.post(headers=self.headers, url=urls, json=data)
                else:
                    response = requests.get(headers=self.headers, url=urls, params=data)

        return response

    def chenk_message(self, result_message, message):
        '''
        获取一个用例的测试结果
        '''
        if result_message == message:
            return True
        else:
            return False

    def chenk_db(self, data, sql_result):
        for key in data.keys():
            if data[key] == sql_result[key]:
                continue
            else:
                return False
        return True

    def chenk_status(self):
        pass

    def run_case(self, index):
        '''
        运行一个请求
        '''
        index = int(index)
        is_login = Case.case[index].get('login')
        if is_login:
            self.headers['token'] = self._sign_in()
        result = []
        result_value = {}
        try:
            name = Case.case[index].get("name")
            method = Case.case[index].get("method", "GET")  # 默认为get请求
            message = Case.case[index].get('message', 'success')
            request_type = Case.case[index].get("type")
            chenk_method = Case.case[index].get('chenk_method', 'message')  # 校验方式，默认message为数据，另外包括db校验，status校验,page
            url = Case.case[index].get('url')
        except KeyError as e:
            console_logger.error('用例%s参数设置有误，请检查参数文件[%s]' % (index, e))
            sys.exit()
        urls = urljoin(self.host, url)
        result.append(index)
        result.append(name)
        result.append(url)
        result.append(method)
        console_logger.info('CASE:%s/NAME:%s/%s:%s' % (index, name, method, urls))
        response = self.requests_case(request_type, index, method, urls)
        if not isinstance(response, int):
            try:
                result_value = response.json()
            except:
                result.append('返回结果不是json格式')
                result.append('status_code:%s' % response.status_code)
                console_logger.error("用例[%s]返回结果错误" % index)
                is_pass = False
            else:
                if chenk_method == 'message':
                    result.append(message)
                    result_message = result_value.get("msg")
                    result.append(result_message)
                    is_pass = self.chenk_message(result_message, message)
                elif chenk_method == 'db':
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
                    request_data = ApiParam.param.get(index)
                    result.append(str(request_data))
                    result.append(str(sql_result))
                    is_pass = self.chenk_db(request_data, sql_result)
                elif chenk_method == "page":
                    pass
                else:
                    pass
        else:
            result.append('用例[%s]执行失败' % response)
            result.append('')
            console_logger.warning('用例[%s]执行失败，无法构建用例[%s]参数，暂不执行该用例' % (response, index))
            is_pass = False
        if is_pass:
            CaseResult.case_result[index] = result_value.get('data')
        return result, is_pass
