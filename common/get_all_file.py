import os

def get_all_yaml(path):
    '''获取所有yaml文件
    @path:文件夹路径
    '''
    result = [os.path.join(path, filename) for filename in os.listdir(
        path) if filename.split('.')[-1] == "yaml"]
    return result

if __name__ == "__main__":
    
    result = get_all_yaml(r"g:\python\APIAutoTest-master\case")
    print(result)
