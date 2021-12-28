import json

import pytest
import allure

from Common.loguru_util import GetLog
from Common.deal_yaml import read_config_yaml, write_extract_yaml, readApiYaml, read_extract_yaml, read_user_defined_variable
from Common.request_util import RequestUtil
from Common.mysql_util import Mysql
from Common.assert_util import AssertUtil

lg = GetLog()
ru = RequestUtil()
mysql = Mysql()

args_all = readApiYaml('../YamlTestCase/web_add_school.yaml').read_testCase_yaml()


@allure.feature('web后台创建学校模块')
# @pytest.mark.run(order=4)
@pytest.mark.addSchool
def test_verify_schoolNameNotDuplicated():
    """校验学校名称是否已经存在于系统内或数据库内，存在需要删除"""
    args = args_all['getSchoolBySchoolName']
    allure.dynamic.story('校验学校名称')
    allure.dynamic.title(args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['webHost'] + args['request']['url']
        method = args['request']['method']
        body = args['request']['body']
        body['schoolName'] = read_user_defined_variable()['schoolInfo']['school_name']
        lg.info("获取的接口请求参数：%s" % args)
        allure.attach(json.dumps(args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, body)
        lg.info(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), args['expect']['msg'])
    if res['data']['schoolNameExits'] is False:
        school_name = args['request']['body']['schoolName']
        del_sql = "DELETE FROM school WHERE name='{}'".format(school_name)
        db_res = mysql.delete_db(del_sql)
        # sql = "select * from school where name='{}'".format(school_name)
        # db_res = mysql.fetch_all(sql)
        if db_res is None:
            lg.info("----------该学校名称成功从数据库删除----------")
        else:
            lg.error("----------从数据库删除该学校名称失败！----------")
    else:
        lg.info(" ============ 学校名称未被使用 ============")


@allure.feature('web后台创建学校模块')
# @pytest.mark.run(order=5)
@pytest.mark.addSchool
def test_add_school():
    """admin管理员创建学校"""
    args = args_all['addSchool']
    allure.dynamic.story('创建学校')
    allure.dynamic.title(args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['webHost'] + args['request']['url']
        method = args['request']['method']
        headers = args['request']['headers']
        body = args['request']['body']
        body['name'] = read_user_defined_variable()['schoolInfo']['school_name']
        body['address'] = read_user_defined_variable()['schoolInfo']['address']
        data = json.dumps(body)
        lg.info("获取的接口请求参数：%s" % args)
        allure.attach(json.dumps(args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        lg.info(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), args['expect']['msg'])
        school_name = args['request']['body']['name']
        sql = "select * from school where name='{}'".format(school_name)
        db_res = mysql.select_db(sql)
        db_schoolName = db_res[0]['name']
        expect_value = read_user_defined_variable()['schoolInfo']['school_name']
        AssertUtil().assert_db(db_schoolName, expect_value)


@allure.feature('web后台创建学校模块')
# @pytest.mark.run(order=6)
@pytest.mark.addSchool
def test_query_school():
    """查询学校列表页面新创建的学校，并获取该学校的school_id"""
    args = args_all['listSchoolQuery']
    allure.dynamic.story('查询学校列表，提取school_id')
    allure.dynamic.title(args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['webHost'] + args['request']['url']
        method = args['request']['method']
        headers = args['request']['headers']
        body = args['request']['body']
        body['schoolName'] = read_user_defined_variable()['schoolInfo']['school_name']
        data = json.dumps(body)
        lg.info("获取的接口请求参数：%s" % args)
        allure.attach(json.dumps(args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        lg.info(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), args['expect']['msg'])
        school_name = res['data']['records'][0]['schoolName']
        expect_value = read_user_defined_variable()['schoolInfo']['school_name']
        AssertUtil().assert_body(school_name, expect_value)
    with allure.step('提取school_id'):
        if res['msg'] == '成功':
            school_id = {"school_id": res['data']['records'][0]['id']}
            write_extract_yaml(school_id)
            lg.info(" ============ school_id提取成功 ============")
        else:
            lg.error(" ============ query学校列表异常！ ============")


@allure.feature('web后台创建学校模块')
# @pytest.mark.run(order=7)
@pytest.mark.addSchool
def test_get_gradeDetail():
    """查询学校详情信息，并且提取该学校的第一个年级grade_id"""
    args = args_all['getGradeDetail']
    allure.dynamic.story('查询学校，提取年级grade_id')
    allure.dynamic.title(args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['webHost'] + args['request']['url']
        method = args['request']['method']
        headers = args['request']['headers']
        body = args['request']['body']
        body['schoolId'] = read_extract_yaml()['school_id']
        data = json.dumps(body)
        lg.info("获取的接口请求参数：%s" % args)
        allure.attach(json.dumps(args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
        lg.info(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), args['expect']['msg'])
        school_name = res['data']['schoolName']
        expect_value = read_user_defined_variable()['schoolInfo']['school_name']
        AssertUtil().assert_body(school_name, expect_value)
    with allure.step('提取grade_id'):
        if res['msg'] == '成功':
            grade_id = {"grade_id": res['data']['gradeAndClassList'][0]['gradeId']}
            write_extract_yaml(grade_id)
            lg.info("============ grade_id提取成功 ============")
        else:
            lg.error(" ============ query学校详情异常！ ============")


@allure.feature('web后台创建学校模块')
# @pytest.mark.run(order=8)
@pytest.mark.addSchool
def test_get_classDetail():
    """查询学校班级信息，并且提取该学校的第一个班级class_id"""
    args = args_all['getClassDetail']
    allure.dynamic.story('查询班级，提取班级class_id')
    allure.dynamic.title(args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['webHost'] + args['request']['url']
        method = args['request']['method']
        headers = args['request']['headers']
        body = args['request']['body']
        body['gradeId'] = read_extract_yaml()['grade_id']
        data = json.dumps(body)
        lg.info("获取的接口请求参数：%s" % args)
        allure.attach(json.dumps(args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
        lg.info(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), args['expect']['msg'])
        class_name = res['data']['records'][0]['className']
        expect_value = args['expect']['className']
        AssertUtil().assert_body(class_name, expect_value)
    with allure.step('提取class_id'):
        if res['msg'] == '成功':
            class_id = {"class_id": res['data']['records'][0]['classId']}
            write_extract_yaml(class_id)
            lg.info("============ class_id提取成功 ============")
        else:
            lg.error(" ============ query班级信息异常！ ============")


if __name__ == '__main__':
    test_query_school()
