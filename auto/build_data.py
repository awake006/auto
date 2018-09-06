import random
import string
import time
import sys
from auto.log import console_logger
from auto import global_data


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
