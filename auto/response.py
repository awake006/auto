from auto.connet_mysql import SelectMySQL
from auto import global_data
from auto.global_data import DB


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
