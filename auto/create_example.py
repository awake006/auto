import os


def create(path):
    base_dir = os.path.join(path, 'auto')
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    case_dir = os.path.abspath(os.path.join(base_dir, 'case/case-example'))
    if not os.path.exists(case_dir):
        os.makedirs(case_dir)
    config_dir = os.path.join(base_dir, 'config')
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)
    get_example = os.path.abspath(os.path.join(case_dir, 'get_example .yaml'))
    post_example = os.path.abspath(os.path.join(case_dir, 'post_example.yaml'))
    put_example = os.path.abspath(os.path.join(case_dir, 'put_example.yaml'))
    delete_example = os.path.abspath(os.path.join(case_dir, 'delete_example.yaml'))
    config_template = os.path.abspath(os.path.join(config_dir, 'config_template.yaml'))
    with open(get_example, 'w', encoding='utf-8') as f:
        case_str = r'''
- name: get request
  method: GET
  chenk_method: db  Verify that the request parameters are consistent with the results stored in the database
  sql: select * from table where img_id=%s,img_id
  url: api/get/example
  id: 1001
  parameter:
    img_id:
      id: 1002  Get img_id from the use case result with case_id of 1002
      value: img_id
        '''
        f.write(case_str)
    with open(post_example, 'w', encoding='utf-8') as f:
        case_str = r'''
- name: post request
  method: POST
  type: file
  chenk_method: db  Verify that the request parameters are consistent with the results stored in the database
  sql: select * from table where contest_id=100 
  url: api/post/example
  id: 1001
  parameter:
    contest_id: 100
    address: shenzhen
    description: str,20 (a string of length 20)
    title: random (random number does not repeat)
    video_time: 20
    img_id:
      id: 1002  Get img_id from the use case result with case_id of 1002
      value: img_id

- name: upload file
  method: POST
  type: file  File upload identifier, when not empty, indicates that the use case is a file upload
  chenk_method: message Verify that the value of the return value is success 
  message: sucess
  url: api/upload/file
  id: 1002
  parameter:
    name: random
    img: file abspath
        '''
        f.write(case_str)
    with open(put_example, 'w', encoding='utf-8') as f:
        case_str = r'''
- name: put request
  method: PUT
  chenk_method: message
  message: success
  url: api/put/example/%s,img_id
  id: 1003
  parameter:
    contest_id: 100
    address: shenzhen
    description: str,20 (a string of length 20)
    title: random (random number does not repeat)
    video_time: 20
    img_id:
      id: 1002  Get img_id from the use case result with case_id of 1002
      value: img_id
        '''
        f.write(case_str)
    with open(delete_example, 'w', encoding='utf-8') as f:
        case_str = r'''
- name: delete request
  method: delete
  chenk_method: message
  message: success
  url: api/delete/example/%s,img_id
  id: 1004
  parameter:
    contest_id: 100
    address: shenzhen
    description: str,20 (a string of length 20)
    title: random (random number does not repeat)
    video_time: 20
    img_id:
      id: 1002  Get img_id from the use case result with case_id of 1002
      value: img_id
        '''
        f.write(case_str)
    with open(config_template, 'w', encoding='utf-8')as f:
        config_str = r'''
- title: 
  case_no: 
  host:
  db_username: 
  db_password: 
  db_host: 
  db: 
  login_url: 
  login_username: 
  login_password: 
  headers:
    Accept-Encoding: gzip;q=1.0,compress;q=0.5
    Accept-Language: zh-Hans-CN;q=1.0,en-CN;q=0.9,zh-Hant-CN;q=0.8
    User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36
        '''
        f.write(config_str)

# if __name__ == "__main__":
#     path = os.getcwd()
#     create(path)
