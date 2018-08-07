import requests

def request(request_type, testcase_id, method, url):
        '''Execute an http request and return the result'''
        requests_dict = {
            'POST': lambda: self._post(request_type, index, urls),
            'GET': lambda: self._put(index, urls),
            'DELETE': lambda: self._delete(index, urls),
            'PUT': lambda: self._put(index, urls)
        }
        return requests_dict[method]()
