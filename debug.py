def requests_case(index, method):
    '''执行一次http请求，返回结果'''
    requests_dict = {
        'POST': lambda: post(index),
        'GET': lambda: put(index),
        'DELETE': lambda: delete(index),
        'PUT': lambda: put(index)
    }
    return requests_dict[method]()


def post(index):
    if index > 100:
        return 100
    else:
        return str(index)


def get(index):

    if index > 100:
        return index
    else:
        return str(index)


def put(index):
    if index > 100:
        return index
    else:
        return str(index)


def delete(index):

    if index > 100:
        return index
    else:
        return str(index)


a = requests_case(100, 'POST')
print(type(a),a)
