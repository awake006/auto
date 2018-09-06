import requests

from auto import global_data
from auto.formater import (format_file_parameter, format_parameter,
                           format_put_delete)


def request(request_type, testcase_id, method, url):
    '''Execute an http request and return the result'''
    requests_dict = {
        'POST': lambda: _post(request_type, testcase_id, url),
        'GET': lambda: _put(testcase_id, url),
        'DELETE': lambda: _delete(testcase_id, url),
        'PUT': lambda: _put(testcase_id, url)
    }
    return requests_dict[method]()


def _post(request_type, testcase_id, url):
    if request_type:
        files = format_file_parameter(testcase_id)
        response = requests.post(headers=global_data.headers, url=url, files=files)
    else:
        data = format_parameter(testcase_id)
        response = requests.post(headers=global_data.headers, url=url, json=data)
    return response


def _get(testcase_id, url):
    data = format_parameter(testcase_id)
    response = requests.get(headers=global_data.headers, url=url, params=data)
    return response


def _put(testcase_id, url):
    result = format_put_delete(url, testcase_id)
    url, data = result
    response = requests.put(headers=global_data.headers, url=url, json=data)
    return response


def _delete(testcase_id, url):
    url, data = format_put_delete(url, testcase_id)
    response = requests.delete(headers=global_data.headers, url=url, json=data)
    return response
