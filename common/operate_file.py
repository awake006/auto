import yaml
import json

def operate_json(path):
    '''
    转化json文件为字典
    '''
    try:
        with open(path,encoding="utf-8") as f:
            result = json.load(f)
            return result
    except FileNotFoundError:
        print("文件不存在")

def operate_yaml(path):
    '''
    转化yaml文件为字典
    '''
    try:
        with open(path,encoding="utf-8")as f:
            result = yaml.load(f)
            return result
    except FileNotFoundError:
        print("文件不存在")

if __name__ == "__main__":
    print(operate_yaml(r"E:\PythonProject\APIAutoTest-master\config\base_info.yaml"))
 



