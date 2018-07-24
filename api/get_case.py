from api.count_case import Case
from api.get_all_file import get_all_yaml
from api.operate_file import operate_yaml


def import_case(path):
    '''
    把用例导入到Case类
    '''
    file = get_all_yaml(path)
    case_list = []
    for i in file:
        case_list += operate_yaml(i)
    for case in case_list:
        Case.all_case[case.get('id')] = case
    print("用例导入成功....")


if __name__ == "__main__":
    import_case(r"d:\python_code\APIAutoTest-master\case\case_yaml")
    print(Case.all_case)
