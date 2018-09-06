import json
import random
import string
import sys
import time
import os
import yaml

from auto import exception, global_data
from auto.log import console_logger
from auto.validator import TestCaseSchema


class OperateFile(object):
    def __init__(self, file):
        self.file = file

    def load_data(self):
        if self.file.split('.')[-1] == "yaml":
            return self.operate_yaml()
        return self.operate_json()

    def operate_json(self):
        '''
        Convert json file to dictionary
        '''
        try:
            with open(self.file, encoding="utf-8") as f:
                result = json.load(f)
                return result
        except FileNotFoundError as e:
            console_logger.error(e)
            sys.exit()

    def operate_yaml(self):
        '''
        Convert yaml file to dictionary
        '''
        try:
            with open(self.file, encoding="utf-8")as f:
                result = yaml.load(f)
                return result
        except FileNotFoundError as e:
            console_logger.error(e)
            sys.exit()


def get_all_yaml(path):
    '''
    Get all yaml files
        @path: folder path
    '''
    try:
        result = [os.path.abspath(os.path.join(path, filename)) for filename in os.listdir(
            path) if filename.split('.')[-1] == "yaml" or filename.split('.')[-1] == 'json']
        return result
    except FileNotFoundError as e:
        console_logger.error(e)
        sys.exit()


def conversion_case(path):
    '''
    Import use cases into the global data
    '''
    file = get_all_yaml(path)
    for i in file:
        operate_file = OperateFile(i)
        testcase_data = operate_file.load_data()
        if not isinstance(testcase_data, list) and testcase_data:
            schema = TestCaseSchema()
            result_errors = schema.load(testcase_data).errors
            if result_errors:
                errors_message = 'testcase file-{} errors-{}'.format(i, result_errors)
                console_logger.error(errors_message)
                sys.exit()
            if testcase_data.get('id') in global_data.testcase.keys():
                console_logger.error('file-{} testcase id {} exist'.format(i, testcase_data.get('id')))
                sys.exit()
            global_data.testcase[testcase_data.get('id')] = testcase_data
            continue
        number = 0
        for testcase in testcase_data:
            number += 1
            if testcase:
                # print(type(testcase))
                schema = TestCaseSchema()
                result_errors = schema.load(testcase).errors
                if result_errors:
                    errors_message = 'testcase file-{} case-{} errors-{}'.format(i, number, result_errors)
                    console_logger.error(errors_message)
                    sys.exit()
                if testcase.get('id') in global_data.testcase.keys():
                    console_logger.error('file-{} case-{} testcase id {} exist'.format(i, number, testcase.get('id')))
                    sys.exit()
                global_data.testcase[testcase.get('id')] = testcase
    console_logger.info('Test case conversion completed')


def set_str(n, index):
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
        message_error_set_str = 'The use case [%s] parameter setting is incorrect, please check the parameter file [%s]' % (
            index, e)
        console_logger.error(message_error_set_str)
        sys.exit()


def set_time():
    '''strftime'''
    now_time = time.strftime("%Y%m%d%H%M%s", time.localtime())
    return now_time


def get_case_id_list():
    testcase_id_list = [i for i in global_data.testcase.keys() if i != '']
    return testcase_id_list


def get_case_data(testcase_id):
    name = global_data.testcase[testcase_id].get("name")
    function_name = global_data.testcase[testcase_id].get('function')
    method = global_data.testcase[testcase_id].get("method", "GET").upper()
    message = global_data.testcase[testcase_id].get('message', 'success')
    request_type = global_data.testcase[testcase_id].get("type")
    check_method = global_data.testcase[testcase_id].get('check_method', 'message').upper()
    url = global_data.testcase[testcase_id].get('url')
    return name, function_name, method, message, request_type, check_method, url
