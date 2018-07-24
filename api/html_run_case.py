import json
import random
import string
import time

import requests
from api.connet_mysql import SelectMySQL
from api.count_case import Case, APIParam, ResultCase

class StartTest(object):
    def __init__(self, base):
        self.host = base.get('host')
        self.port = base.get('port')
        self.headers = base.get('headers')
        if base.get("number"):
            self.number = base.get("number").split(',')
        else:
            self.number = self._get_case_number()
        self.results = []
        self.db = base.get('db')
        self.db_username = base.get("db_username")
        self.db_password = base.get('db_password')
        self.db_host = base.get("db_host")
        self.login_url = base.get("login_url")
        self.login_username = base.get("login_username")
        self.login_password = base.get("login_password")

    def _get_case_number(self):
        case_number = []
        for key in Case.all_case.keys():
            case_number.append(key)
        return case_number

    def _sign_in(self):
        '''
        获取用户登录token
        支持帐号登录可以写一个登录的方法
        '''
        data = {'username':self.login_username,'password':self.login_password}
        response = requests.post(url=self.login_url,json=data)
        return response.headers['token']

    def _set_str(self,n):
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
            raise e

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
            params = Case.all_case.get(index)['params']
        except KeyError as e:
            raise e
        for key in params:
            if isinstance(params.get(key), dict):
                """
                字典，需要从别的接口获取数据
                """
                case_dict = params.get(key)
                case_id = case_dict.get('id')
                case_data = ResultCase.case_result.get(case_id)
                if case_data:
                    case_result = case_data
                else:
                    self.run_case(case_id)
                    case_result = ResultCase.case_result.get(case_id)
                if case_result:
                    if type(case_result) != list:
                        v = case_result
                    else:
                        v = case_result[0]
                    data[key] = (None, str(v.get(case_dict.get('value'))))
            elif params.get(key).split(',')[0] == 'get_name':
                data[key] = self._set_str(params.get(key).split(',')[1])
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
        APIParam.param[index] = data
        return data

    def _format_param(self, index):
        '''
        格式化获取参数
        '''
        data = {}
        try:
            params = Case.all_case.get(index)['params']
        except KeyError as e:
            raise e

        for key in params:
            if isinstance(params.get(key), dict):
                """
                字典，需要从别的接口获取数据
                """
                case_dict = params.get(key)
                case_id = case_dict.get('id')
                case_data = ResultCase.case_result.get(case_id)
                if case_data:
                    case_result = case_data
                else:
                    self.run_case(case_id)
                    case_result = ResultCase.case_result.get(case_id)
                if case_result:
                    if type(case_result) != list:
                        v = case_result
                    else:
                        v = case_result[0]
                    data[key] = v.get(case_dict.get('value'))
            elif params.get(key).split(',')[0] == 'get_name':
                data[key] = self._set_str(params.get(key).split(',')[1])
            elif params.get(key) == "random":
                data[key] = self._set_time()
            else:
                data[key] = params.get(key)
        APIParam.param[index] = data
        return data

    def _format_put_and_delete(self,url,index):
        data = {}
        return url,data

    def requests_case(self,request_type,index,method,urls):
        '''执行一次http请求，返回结果'''
        if request_type:
            files = self._format_file_param(index)
            response = requests.post(headers=self.headers,url=urls,files=files)
        else:
            if method == ("PUT" or "DELETE"):
                urls,data = self._format_put_and_delete(urls,index)
                if method == "PUT":
                    response = requests.post(headers=self.headers,url=urls,json=data)
                elif method == "DELETE":
                    response = requests.delete(headers=self.headers,url=urls,json=data)
            else:
                data = self._format_param(index)
                if method == "POST":
                    response = requests.post(headers=self.headers,url=urls,json=data)
                else:
                    response = requests.get(headers=self.headers,url=urls,params=data)
        return response

    def chenk_message(self, result_message, message):
        '''
        获取一个用例的测试结果
        '''
        if result_message == message:
            return True
        else:
            return False

    def chenk_db(self,data,sql_result):
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
        is_login = Case.all_case[index].get('login')
        if is_login:
            self.headers['token'] = self._sign_in()
        result = []
        result_value = {}
        name = Case.all_case[index].get("name","case_name_is_none")
        method = Case.all_case[index].get("method","GET")#默认为get请求
        message = Case.all_case[index].get('message')
        request_type = Case.all_case[index].get("type")
        chenk_method = Case.all_case[index].get('chenk_method','message')#校验方式，默认message为数据，另外包括db校验，status校验,page
        url = Case.all_case[index].get('url')
        if url:
            urls = self.host + url
            result.append(index)
            result.append(name)
            result.append(url)
            result.append(method)
            response = self.requests_case(request_type,index,method,urls)
            try:
                result_value = response.json()
            except:
                result.append('返回值必须为json格式')
                result.append('返回结果格式错误，status_code:%s'%response.status_code)
                is_pass = False
            else:
                if chenk_method == 'message':
                    result.append(message)
                    result_message = result_value.get("msg")
                    result.append(result_message)
                    is_pass = self.chenk_message(result_message,message)
                elif chenk_method == 'db':
                    sql = Case.all_case[index].get('sql')
                    if '%' in sql:
                        for value in APIParam.param.get(index).values():
                            if isinstance(value,list):
                                continue
                            param_value = value
                            break
                        sql = sql%param_value
                    db = SelectMySQL(self.db_host,self.db_username,self.db_password,self.db)
                    db.connect()
                    sql_result = db.select_one(sql)
                    request_data = APIParam.param.get(index)
                    result.append(str(request_data))
                    result.append(str(sql_result))
                    is_pass = self.chenk_db(request_data,sql_result)
                elif chenk_method == "page":
                    pass
                else:
                    pass
                if is_pass:
                    ResultCase.case_result[index] = result_value.get('data')
        else:
            url = 'null'
            result.append(index)
            result.append(name)
            result.append(url)
            result.append(method)
            result.append('url不能为空')
            result.append('url为空')
            is_pass = False
        return result,is_pass
        
