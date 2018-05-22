import requests

response = requests.get('https://www.baidu.com')
try:
    result_value = response.json()
except:
    print('返回值必须为json格式')
    print('返回结果格式错误，status_code:%s'%response.status_code)