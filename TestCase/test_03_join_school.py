import json
import pytest
import allure
from Common.loguru_util import GetLog
from Common.deal_yaml import readApiYaml, read_config_yaml, read_extract_yaml, write_extract_yaml, read_user_defined_variable
from Common.request_util import RequestUtil
from Common.assert_util import AssertUtil
from Common.mysql_util import Mysql

lg = GetLog()
ru = RequestUtil()
mysql = Mysql()

homepage_args = readApiYaml('../YamlTestCase/teacher_homePage.yaml').read_testCase_yaml()


@allure.feature('教师入校申请模块')
# @pytest.mark.run(order=0)
@pytest.mark.joinSchool
@pytest.mark.parametrize('homepage_args', homepage_args)
def test_teacher_home_page(homepage_args):
    """查询教师用户我的主页接口，并且提取userId"""
    allure.dynamic.story('教师端我的主页')
    allure.dynamic.title(homepage_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + homepage_args['request']['url']
        method = homepage_args['request']['method']
        headers = homepage_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        lg.info("获取的接口请求参数：%s" % homepage_args)
        allure.attach(json.dumps(homepage_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), homepage_args['expect']['msg'])
    with allure.step('提取teacher_userId'):
        if res['msg'] == '成功':
            teacher_userId = {"teacher_userId": res['data']['userInfo']['userId']}
            write_extract_yaml(teacher_userId)
            lg.info("============ teacher_userId提取成功 ============")
        else:
            lg.error("============ query教师我的主页异常！ ============")


joinSchool_args = readApiYaml('../YamlTestCase/teacher_joinSchool.yaml').read_testCase_yaml()


@allure.feature('教师入校申请模块')
# @pytest.mark.run(order=10)
@pytest.mark.joinSchool
@pytest.mark.parametrize('joinSchool_args', joinSchool_args)
def test_join_school(joinSchool_args):
    """预设教师手机号登录后，提交入校申请，并且从数据库验证申请记录是否存在"""
    allure.dynamic.story('教师申请入校')
    allure.dynamic.title(joinSchool_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + joinSchool_args['request']['url']
        method = joinSchool_args['request']['method']
        headers = joinSchool_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = joinSchool_args['request']['body']
        body['schoolId'] = read_extract_yaml()['school_id']
        body['classId'] = read_extract_yaml()['class_id']
        body['realName'] = read_user_defined_variable()['name']['teacher_name']
        body['mobile'] = read_user_defined_variable()['mobile']['teacher_mobile']
        data = json.dumps(body)
        lg.info("获取的接口请求参数：%s" % joinSchool_args)
        allure.attach(json.dumps(joinSchool_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), joinSchool_args['expect']['msg'])
        school_id = read_extract_yaml()['school_id']
        teacher_userId = read_extract_yaml()['teacher_userId']
        sql = "select * from school_teacher_review where school_id ='{}' and user_id='{}'".format(school_id,
                                                                                                  teacher_userId)
        db_res = mysql.select_db(sql)
        db_teacherName = db_res[0]['teacher_name']
        expect_value = read_user_defined_variable()['name']['teacher_name']
        AssertUtil().assert_db(db_teacherName, expect_value)


args_all = readApiYaml('../YamlTestCase/web_add_school.yaml').read_testCase_yaml()


@allure.feature('教师入校申请模块')
# @pytest.mark.run(order=9)
@pytest.mark.joinSchool
def test_teacher_review_list():
    """web管理后台admin查询教师申请列表页面，并且提取申请记录的review_id"""
    args = args_all['listTeacherReview']
    allure.dynamic.story('admin查询教师申请，提取review_id')
    allure.dynamic.title(args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['webHost'] + args['request']['url']
        method = args['request']['method']
        headers = args['request']['headers']
        data = args['request']['body']
        data['reviewTeacher'] = read_user_defined_variable()['name']['teacher_name']
        lg.info("获取的接口请求参数：%s" % args)
        allure.attach(json.dumps(args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
        lg.info(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), args['expect']['msg'])
        review_teacher = res['data']['records'][0]['reviewTeacherName']
        expect_value = read_user_defined_variable()['name']['teacher_name']
        AssertUtil().assert_body(review_teacher, expect_value)
    with allure.step('提取teacher_review_id'):
        if res['msg'] == '成功':
            teacher_review_id = {"teacher_review_id": res['data']['records'][0]['reviewId']}
            write_extract_yaml(teacher_review_id)
            lg.info("============ review_id提取成功 ============")
        else:
            lg.error(" ============ query教师申请信息异常！ ============")


@allure.feature('教师入校申请模块')
# @pytest.mark.run(order=10)
@pytest.mark.joinSchool
def test_update_teacher_review():
    """web管理后台admin更新教师申请状态为通过，并且通过查询数据库该申请记录，验证通过申请"""
    args = args_all['updateTeacherReviewStatus']
    allure.dynamic.story('admin通过教师申请')
    allure.dynamic.title(args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['webHost'] + args['request']['url']
        method = args['request']['method']
        headers = args['request']['headers']
        body = args['request']['body']
        body['reviewIds'] = [read_extract_yaml()['teacher_review_id']]
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
        review_id = read_extract_yaml()['teacher_review_id']
        sql = "select * from school_teacher_review where id='{}' and `status`=1".format(review_id)
        db_res = mysql.select_db(sql)
        db_status = db_res[0]['status']
        expect_value = args['expect']['sql']['status']
        AssertUtil().assert_db(db_status, expect_value)


@allure.feature('教师入校申请模块')
# @pytest.mark.run(order=11)
@pytest.mark.joinSchool
def test_delete_teacher_review():
    """web管理后台admin删除教师审批记录"""
    args = args_all['deleteTeacherReview']
    allure.dynamic.story('admin删除教师审批记录')
    allure.dynamic.title(args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['webHost'] + args['request']['url']
        method = args['request']['method']
        headers = args['request']['headers']
        body = args['request']['body']
        body['reviewIds'] = [read_extract_yaml()['teacher_review_id']]
        data = json.dumps(body)
        lg.info("获取的接口请求参数：%s" % args)
        allure.attach(json.dumps(args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        lg.info(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), args['expect']['msg'])
        review_id = read_extract_yaml()['teacher_review_id']
        sql = "select * from school_teacher_review where id ='{}' and delete_flag=1;".format(review_id)
        db_res = mysql.select_db(sql)
        db_delete_flag = db_res[0]['delete_flag']
        expect_value = args['expect']['sql']['delete_flag']
        AssertUtil().assert_db(db_delete_flag, expect_value)


@allure.feature('教师入校申请模块')
# @pytest.mark.run(order=12)
@pytest.mark.joinSchool
def test_query_teacher():
    """web管理后台admin查询教师列表页面，是否存在通过申请的老师"""
    args = args_all['listTeacherQuery']
    allure.dynamic.story('admin教师列表查询')
    allure.dynamic.title(args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['webHost'] + args['request']['url']
        method = args['request']['method']
        # headers = args['request']['headers']
        body = args['request']['body']
        body['teacherNameOrMobile'] = read_user_defined_variable()['name']['teacher_name']
        res = ru.run_main(method, url, body)
        lg.info("获取的接口请求参数：%s" % args)
        allure.attach(json.dumps(args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        lg.info(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), args['expect']['msg'])
        user_id = res['data']['records'][0]['userId']
        school_id = res['data']['records'][0]['schoolId']
        sql = "select * from user_school where user_id={} and school_id={} and user_role=2".format(user_id, school_id)
        db_res = mysql.select_db(sql)
        db_userName = db_res[0]['user_name']
        expect_value = read_user_defined_variable()['name']['teacher_name']
        AssertUtil().assert_db(db_userName, expect_value)


if __name__ == '__main__':
    r = test_join_school()
    print(r)
