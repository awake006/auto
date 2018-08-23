import json
import os
import sys

import yaml

from auto import global_data
from auto.log import console_logger
from auto import exception


def operate_json(path):
    '''
    Convert json file to dictionary
    '''
    try:
        with open(path, encoding="utf-8") as f:
            result = json.load(f)
            return result
    except FileNotFoundError as e:
        console_logger.error(e)
        sys.exit()


def operate_yaml(path):
    '''
    Convert yaml file to dictionary
    '''
    try:
        with open(path, encoding="utf-8")as f:
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
        result = [os.path.join(path, filename) for filename in os.listdir(
            path) if filename.split('.')[-1] == "yaml"]
        return result
    except FileExistsError as e:
        console_logger.error(e)
        sys.exit()


def conversion_case(path):
    '''
    Import use cases into the global data
    '''
    file = get_all_yaml(path)
    testcase_list = []
    for i in file:
        testcase_list += operate_yaml(i)
    for testcase in testcase_list:
        if testcase and chenk_case(testcase):
            global_data.testcase[testcase.get('id')] = testcase
    console_logger.info('Test case conversion completed')


def chenk_case(case_dict):
    case_required_data = ['name', 'function', 'id', 'url']
    for data in case_required_data:
        if data not in case_dict.keys():
            msg = 'case[%s] error' % data.get('id')
            console_logger.error(msg)
            raise exception.CaseRequiredDataException(msg)
    return True


if __name__ == "__main__":
    print(get_all_yaml(r"case/"))
