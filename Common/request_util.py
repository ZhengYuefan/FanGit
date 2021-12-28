
import json
import requests


class RequestUtil(object):

    def get_mode(self, url, headers=None, data=None):
        # 忽略不安全的请求警告信息
        requests.packages.urllib3.disable_warnings()
        # 遇到requests的ssl验证，若想直接跳过不验证，设置verify=False即可
        # response = requests.get(url=url, headers=headers, data=data, verify=False)
        if data is None:
            response = requests.get(url=url, headers=headers, verify=False)
        else:
            if headers is not None:
                response = requests.get(url=url, headers=headers, data=data, verify=False)
            else:
                response = requests.get(url=url, data=data, verify=False)
        return response.json()

    def post_mode(self, url, headers=None, data=None, files=None):
        # 忽略不安全的请求警告信息
        requests.packages.urllib3.disable_warnings()

        # response = requests.post(url=url, headers=headers, data=data, verify=False)
        if files is not None:
            response = requests.post(url=url, headers=headers, data=data, files=files, verify=False)
        else:
            if headers is not None:
                response = requests.post(url=url, headers=headers, data=data, verify=False)
            else:
                response = requests.post(url=url, data=data, verify=False)
        return response.json()

    def put_mode(self, url, headers, data):
        # 忽略不安全的请求警告信息
        requests.packages.urllib3.disable_warnings()
        response = requests.put(url=url, headers=headers, data=data, verify=False)
        return response.json()

    def delete_mode(self, url, headers, data):
        # 忽略不安全的请求警告信息
        requests.packages.urllib3.disable_warnings()
        response = requests.delete(url=url, headers=headers, data=data)
        return response.json()

    def run_main(self, method, url, data=None, headers=None, files=None):
        if method == 'get':
            return self.get_mode(url, headers, data)
        elif method == 'post':
            return self.post_mode(url, headers, data, files)
        elif method == 'put':
            return self.put_mode(url, headers, data)
        elif method == 'delete':
            return self.delete_mode(url, headers, data)
        else:
            return {'code': '请求方法错误，请使用get/post/put/delete'}


if __name__ == '__main__':
    rm = RequestUtil()
    method = 'put'
    url = 'http://192.168.0.214:9200/v1/manage/school/addSchool'
    headers = {"Content-Type": "application/json"}
    body = {
        "name": "Test测试学院",
        "type": 0,
        "address": "杭州市滨江区江陵路聚光中心",
        "classList": [{
            "gradeName": 0,
            "classNumber": 1
        }]
    }
    data = json.dumps(body)
    # res = rm.post_mode(url, headers, bodyData)
    res = rm.run_main(method, url, data, headers, files=None)
    print(type(res))
    print(res)
