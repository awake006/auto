import json
import os
import sys

import yaml

from auto import global_data
from auto.log import console_logger
from auto import exception
from auto.validator import TestCaseSchema


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
        testcase_list = operate_yaml(i)
        number = 0
        for testcase in testcase_list:
            number += 1
            if testcase:
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


if __name__ == "__main__":
    print(get_all_yaml(r"case/"))
