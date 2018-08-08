import sys

from auto import build_data, global_data
from auto.log import console_logger


def format_file_parameters(testcase_id):
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
                    testcase_result = global_data.testcase_result.get(old_case_id)
                    if not testcase_result:
                        return int(old_case_id)

                if isinstance(testcase_result, list):
                    testcase_result = testcase_result[0]

                data[key] = (None, str(testcase_result.get(testcase_dict.get('value'))))

            elif str(parameter.get(key)).split(',')[0] == 'str':
                data[key] = (None, build_data.set_str(parameter.get(key).split(',')[1], testcase_id))

            elif parameter.get(key) == "random":
                data[key] = (None, str(build_data.set_time()))

            elif key == "video":
                data[key] = ("video.mp4", open(
                    parameter.get(key), 'rb'), "video/mp4")

            elif key == "img":
                data[key] = ('img.png', open(
                    parameter.get(key), 'rb'), "image/jpg/png/jpeg")
            else:
                data[key] = (None, str(parameter.get(key)))

        global_data.testcase_parameter[testcase_id] = data
        return data
    except (KeyError, FileNotFoundError) as e:
        message_error_format_param = 'The use case [%s] parameter setting is incorrect, please check the parameter file [%s]' % (
            testcase_id, e)
        console_logger.error(message_error_format_param)
        raise e


def format_parameter(testcase_id):
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
                    testcase_result = global_data.testcase_result.get(old_case_id)
                    if not testcase_result:
                        return int(old_case_id)

                if isinstance(testcase_result, list):
                    testcase_result = testcase_result[0]

                data[key] = testcase_result.get(testcase_dict.get('value'))

            elif str(parameter.get(key)).split(',')[0] == 'str':
                data[key] = build_data.set_str(parameter.get(key).split(',')[1], testcase_id)

            elif parameter.get(key) == "random":
                data[key] = build_data.set_time()

            else:
                data[key] = parameter.get(key)

        global_data.testcase_parameter[testcase_id] = data
        return data
    except (KeyError, FileNotFoundError) as e:
        message_error_format_param = 'The use case [%s] parameter setting is incorrect, please check the parameter file [%s]' % (
            testcase_id, e)
        console_logger.error(message_error_format_param)
        raise e


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
                    testcase_result = global_data.testcase_result.get(old_case_id)
                    if not testcase_result:
                        return int(old_case_id)

                if isinstance(testcase_result, list):
                    testcase_result = testcase_result[0]

                new_url = url % testcase_result.get(testcase_dict.get('value'))

            elif str(parameter.get(key)).split(',')[0] == 'str':
                data[key] = build_data.set_str(parameter.get(key).split(',')[1], testcase_id)

            elif parameter.get(key) == "random":
                data[key] = build_data.set_time()

            else:
                data[key] = parameter.get(key)

        global_data.testcase_parameter[testcase_id] = data
        return new_url, data
    except (KeyError, FileNotFoundError) as e:
        message_error_format_param = 'The use case [%s] parameter setting is incorrect, please check the parameter file [%s]' % (
            testcase_id, e)
        console_logger.error(message_error_format_param)
        raise e
