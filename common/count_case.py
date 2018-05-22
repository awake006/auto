#数据存储
class CountResult(object):
    '''用例结果统计 result: 
    case
    '''
    success = 0
    fail = 0
    total = 0
    result = {}

class Case(object):
    '''用例存储 {
        case_id1:
        {caseinfo:info,prarm:{key1:[value0,value1],key2:value2}},
        case_id2:{caseinfo:info,prarm:{key1:[value0,value1],key2:value2}}
    }'''
    all_case = {}

class ResultCase():
    '''用例结果参数存储，以备其他用例调用  {
        case_id1:{response:info,data:{key:value}},
        case_id2:{response:info,data:[{key:value},{key:value}]}
    }'''

    case_result = {}

class APIParam():
    '''提交参数存储，用于与数据库校验结果 {
        case_id:[{key:value},{key:value}],case_id1:{key:value},
    }'''
    param = {}
