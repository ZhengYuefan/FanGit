import json

import pytest
import allure

from Common.loguru_util import GetLog
from Common.deal_yaml import read_config_yaml, write_extract_yaml, readApiYaml, read_extract_yaml
from Common.request_util import RequestUtil
from Common.mysql_util import Mysql
from Common.assert_util import AssertUtil

lg = GetLog()
ru = RequestUtil()
mysql = Mysql()

args_all = readApiYaml('../YamlTestCase/web_add_school.yaml').read_testCase_yaml()


@allure.feature('web后台删除学校模块')
# @pytest.mark.second_to_last
@pytest.mark.deleteSchool
def test_delete_class():
    """删除班级"""
    args = args_all['deleteClasses']
    allure.dynamic.story('删除班级')
    allure.dynamic.title(args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['webHost'] + args['request']['url']
        method = args['request']['method']
        headers = args['request']['headers']
        body = args['request']['body']
        body['classId'] = read_extract_yaml()['class_id']
        lg.info("获取的接口请求参数：%s" % args)
        allure.attach(json.dumps(args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, body, headers)
        lg.info(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), args['expect']['msg'])
        school_id = read_extract_yaml()['school_id']
        class_id = read_extract_yaml()['class_id']
        sql = "select * from class where id={} and school_id={};".format(class_id, school_id)
        db_res = mysql.select_db(sql)
        db_delete_flag = db_res[0]['delete_flag']
        expect_value = args['expect']['sql']['delete_flag']
        AssertUtil().assert_db(db_delete_flag, expect_value)


@allure.feature('web后台删除学校模块')
# @pytest.mark.last
@pytest.mark.deleteSchool
def test_delete_school():
    """删除学校"""
    args = args_all['deleteSchool']
    allure.dynamic.story('删除学校')
    allure.dynamic.title(args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['webHost'] + args['request']['url']
        method = args['request']['method']
        headers = args['request']['headers']
        body = args['request']['body']
        body['schoolId'] = read_extract_yaml()['school_id']
        lg.info("获取的接口请求参数：%s" % args)
        allure.attach(json.dumps(args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, body, headers)
        lg.info(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), args['expect']['msg'])
        school_id = read_extract_yaml()['school_id']
        sql = "select * from school where id={}".format(school_id)
        db_res = mysql.select_db(sql)
        db_delete_flag = db_res[0]['delete_flag']
        expect_value = args['expect']['sql']['delete_flag']
        AssertUtil().assert_db(db_delete_flag, expect_value)
