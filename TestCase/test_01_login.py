import allure

from Common.loguru_util import GetLog
from Common.request_util import RequestUtil
from Common.deal_yaml import readApiYaml, read_config_yaml, write_extract_yaml, read_user_defined_variable
import pytest
import json
from Common.assert_util import AssertUtil

lg = GetLog()
ru = RequestUtil()

teacher_args = readApiYaml('../YamlTestCase/login_teacher.yaml').read_testCase_yaml()


@allure.feature('用户登录模块')
# @allure.link(url='https://www.baidu.com/', name='link_url')
# @allure.issue(url='https://www.baidu.com/', name='issue_url')
# @allure.testcase(url='https://www.baidu.com/', name='testcase_url')
# @pytest.mark.run(order=2)
@pytest.mark.login
@pytest.mark.parametrize('teacher_args', teacher_args)
def test_teacher_login(teacher_args):
    """测试老师角色用户登录，采用正向和反向场景来针对手机号和用户类型id进行组合后验证"""
    allure.dynamic.story('老师用户登录')
    allure.dynamic.title(teacher_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + teacher_args['request']['url']
        method = teacher_args['request']['method']
        headers = teacher_args['request']['headers']
        body = teacher_args['request']['body']
        body['mobile'] = read_user_defined_variable()['mobile']['teacher_mobile']
        data = json.dumps(body)
        allure.attach(json.dumps(teacher_args, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, data, headers, files=None)
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), teacher_args['expect']['msg'])
    with allure.step('提取teacher_token'):
        if res['msg'] == '成功':
            teacher_token = {"teacher_token": res['data']['token']}
            write_extract_yaml(teacher_token)
            lg.info(" ============ teacher_token提取成功 ============")
        else:
            lg.error(" ============ teacher用户登录异常！ ============")
    lg.info(teacher_args)
    lg.info(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False))


student_args = readApiYaml('../YamlTestCase/login_student.yaml').read_testCase_yaml()


@allure.feature('用户登录模块')
# @pytest.mark.run(order=3)
@pytest.mark.login
@pytest.mark.parametrize('student_args', student_args)
def test_student_login(student_args):
    """测试学生角色用户登录，采用正向和反向场景来针对手机号和用户类型id进行组合后验证"""
    allure.dynamic.story('学生用户登录')
    with allure.step('发送请求'):
        allure.dynamic.title(student_args['name'])
        url = read_config_yaml()['appHost'] + student_args['request']['url']
        method = student_args['request']['method']
        headers = student_args['request']['headers']
        body = student_args['request']['body']
        body['mobile'] = read_user_defined_variable()['mobile']['student_mobile']
        data = json.dumps(body)
        allure.attach(json.dumps(student_args, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, data, headers, files=None)
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), student_args['expect']['msg'])
    with allure.step('提取student_token'):
        if res['msg'] == '成功':
            student_token = {"student_token": res['data']['token']}
            write_extract_yaml(student_token)
            lg.info(" ============ student_token提取成功 ============")
        else:
            lg.error(" ============ student用户登录异常！ ============")


admin_args = readApiYaml('../YamlTestCase/web_login_admin.yaml').read_testCase_yaml()


@allure.feature('用户登录模块')
# @pytest.mark.run(order=1)
@pytest.mark.login
@pytest.mark.parametrize('admin_args', admin_args)
def test_admin_login(admin_args):
    """测试admin角色用户登录管理后台，采用正向和反向场景来针对手机号和用户类型id进行组合后验证"""
    allure.dynamic.story('admin用户登录管理后台')
    allure.dynamic.title(admin_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['webHost'] + admin_args['request']['url']
        method = admin_args['request']['method']
        headers = admin_args['request']['headers']
        body = admin_args['request']['body']
        data = json.dumps(body)
        allure.attach(json.dumps(admin_args, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, data, headers, files=None)
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(res['msg'], admin_args['expect']['msg'])
        lg.info("接口请求参数：%s" % admin_args)
        lg.info("接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False))


if __name__ == '__main__':
    test_teacher_login()
