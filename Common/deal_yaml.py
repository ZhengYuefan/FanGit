import os
import yaml
import time


def get_project_path():
    """获得项目路径"""
    realPath = os.path.dirname(__file__).split('Common')[0]
    return realPath


def read_config_yaml():
    """读取全局配置yaml文件"""
    with open(str(get_project_path()) + 'Config/config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
        return config


def read_extract_yaml():
    """读取提取变量yaml文件"""
    with open(str(get_project_path()) + 'Config/extract.yaml', 'r', encoding='utf-8') as f:
        extract = yaml.load(f.read(), Loader=yaml.FullLoader)
        return extract


def write_extract_yaml(extract_dict):
    """向提取变量yaml文件写入数据"""
    with open(str(get_project_path()) + 'Config/extract.yaml', 'a') as f:
        yaml.dump(extract_dict, f)


def read_user_defined_variable():
    """读取用户自定义变量yaml文件"""
    with open(str(get_project_path()) + 'Config/user_defined_variable.yaml', 'r', encoding='utf-8') as f:
        custom_variable = yaml.load(f.read(), Loader=yaml.FullLoader)
        return custom_variable


def clear_extract_yaml():
    """清空提取参数yaml文件"""
    with open(str(get_project_path()) + 'Config/extract.yaml', 'w') as f:
        f.truncate()


# 读取用例内容
class readApiYaml(object):
    def __init__(self, yaml_name):
        self.yaml_name = yaml_name

    def read_testCase_yaml(self):
        """读取测试用例yaml文件"""
        with open(str(get_project_path()) + 'TestCase/' + self.yaml_name, 'r', encoding='utf-8') as f:
            content = yaml.load(f, Loader=yaml.FullLoader)
            return content

    def get_url(self, content):
        conf = read_config_yaml()
        host = conf['host']
        api_url = host + content['request']['url']
        print("接口路径：", api_url)
        return api_url

    def get_method(self, content):
        print("请求方式：", content['request']['method'])
        return content['request']['method']

    def get_body(self, content):
        return content['request']['body']

    def get_headers(self, content):
        return content['request']['headers']

    def get_name(self, content):
        print("接口名称：", content['name'])
        return content['request']['name']

    # 获取响应结果的预期结果
    def get_expected(self, content):
        expected = content['request']['expected']
        return expected

    def get_time(self):
        # 以毫秒为单位的时间戳
        get_now_milli_time = int(time.time() * 1000)
        print(get_now_milli_time)


if __name__ == '__main__':
    r = readApiYaml('login_teacher.yaml')
    t = r.read_testCase_yaml()
    w = r.get_body(t)
    print(w)