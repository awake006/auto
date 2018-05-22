import requests

def sign_in():
    urls = 'http://api.admin.dianping.lubanfenqi.com/admin/login'
    datas = {'username':'admin','password':123456}
    response = requests.post(url=urls,json=datas)
    return response.headers['token']
headers = {}
headers['token'] = sign_in()

url = 'http://api.admin.dianping.lubanfenqi.com/projects/tags/1/enable'

data = {}
r = requests.put(url=url,headers=headers,json=data)
print(r.url)
print(r.text)