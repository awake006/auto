# data storage
class Count(object):
    '''Use case results statistics
    result: 
    case
    '''
    success = 0
    fail = 0
    total = 0
    result = {}


class Case(object):
    '''
    Use case storage{
        case_id1:{caseinfo:info,prarm:{key1:[value0,value1],key2:value2}},
        case_id2:{caseinfo:info,prarm:{key1:[value0,value1],key2:value2}}
    }
    '''
    case = {}


class CaseResult(object):
    '''
    Use case result parameter storage for other use case calls  
    {
        case_id1:{response:info,data:{key:value}},
        case_id2:{response:info,data:[{key:value},{key:value}]}
    }
    '''
    case_result = {}


class ApiParam():
    '''
    Submit parameter storage for verification results with the database 
    {
        case_id:[{key:value},{key:value}],case_id1:{key:value},
    }
    '''
    param = {}
