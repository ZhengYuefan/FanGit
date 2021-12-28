import json
import pytest
import allure
from Common.deal_yaml import readApiYaml, read_config_yaml, read_extract_yaml, write_extract_yaml, read_user_defined_variable
from Common.request_util import RequestUtil
from Common.loguru_util import GetLog
from Common.assert_util import AssertUtil
from Common.mysql_util import Mysql

lg = GetLog()
ru = RequestUtil()
mysql = Mysql()

homePage_args = readApiYaml("../YamlTestCase/student_homePage.yaml").read_testCase_yaml()


@allure.feature('学生入班申请模块')
# @pytest.mark.run(order=1)
@pytest.mark.joinClass
@pytest.mark.parametrize("homePage_args", homePage_args)
def test_student_home_page(homePage_args):
    """查询学生用户我的主页接口，并且提取userId"""
    allure.dynamic.story('学生端我的主页')
    allure.dynamic.title(homePage_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + homePage_args['request']['url']
        method = homePage_args['request']['method']
        headers = homePage_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['student_token']
        lg.info("获取的接口请求参数：%s" % homePage_args)
        allure.attach(json.dumps(homePage_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应参数')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), homePage_args['expect']['msg'])
    with allure.step('提取student_userId'):
        if res['msg'] == '成功':
            student_userId = {"student_userId": res['data']['userInfo']['userId']}
            write_extract_yaml(student_userId)
            lg.info("---------- student_userId提取成功 ----------")
        else:
            lg.error("---------- query学生我的主页异常！ ----------")


joinClass_args = readApiYaml("../YamlTestCase/student_joinClass.yaml").read_testCase_yaml()


@allure.feature('学生入班申请模块')
# @pytest.mark.run(order=2)
@pytest.mark.joinClass
@pytest.mark.parametrize("joinClass_args", joinClass_args)
def test_join_class(joinClass_args):
    """预设学生手机号登录后，提交入校申请，并且从数据库验证申请记录是否存在"""
    allure.dynamic.story('学生申请入班')
    allure.dynamic.title(joinClass_args['name'])
    with allure.step('查询数据库'):
        student_userId = read_extract_yaml()['student_userId']
        sql = "select * from school_student_review where user_id={};".format(student_userId)
        db_res = mysql.select_db(sql)
        if db_res is None:
            lg.info("---------- 该学生未提交过入班申请 ----------")
        else:
            del_sql = "delete from school_student_review where user_id={};".format(student_userId)
            mysql.delete_db(del_sql)
            lg.info("---------- 成功删除该学生入班申请历史记录 ----------")
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + joinClass_args['request']['url']
        method = joinClass_args['request']['method']
        headers = joinClass_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['student_token']
        body = joinClass_args['request']['body']
        body['schoolId'] = read_extract_yaml()['school_id']
        body['classId'] = read_extract_yaml()['class_id']
        body['realName'] = read_user_defined_variable()['name']['student_name']
        data = json.dumps(body)
        lg.info("获取的接口请求参数：%s" % joinClass_args)
        allure.attach(json.dumps(joinClass_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应参数')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), joinClass_args['expect']['msg'])
        school_id = read_extract_yaml()['school_id']
        user_id = read_extract_yaml()['student_userId']
        sql = "select * from school_student_review where school_id ={} and user_id={}".format(school_id, user_id)
        db_res = mysql.select_db(sql)
        db_studentName = db_res[0]['student_name']
        expect_value = read_user_defined_variable()['name']['student_name']
        AssertUtil().assert_db(db_studentName, expect_value)


reviewList_args = readApiYaml("../YamlTestCase/student_reviewList.yaml").read_testCase_yaml()


@allure.feature('学生入班申请模块')
# @pytest.mark.run(order=3)
@pytest.mark.joinClass
@pytest.mark.parametrize("reviewList_args", reviewList_args)
def test_students_review_list(reviewList_args):
    """老师端查询学生审批列表，是否存在学生入班申请记录，并且提取申请记录的review_id"""
    allure.dynamic.story('老师端查询学生申请，提取review_id')
    allure.dynamic.title(reviewList_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + reviewList_args['request']['url']
        method = reviewList_args['request']['method']
        headers = reviewList_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = reviewList_args['request']['body']
        body['classIds'] = read_extract_yaml()['class_id']
        body['studentName'] = read_user_defined_variable()['name']['student_name']
        lg.info("获取的接口请求参数：%s" % reviewList_args)
        allure.attach(json.dumps(reviewList_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, body, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应参数')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), reviewList_args['expect']['msg'])
        if res['msg'] == '成功':
            res_list = res['data']
            for stu in res_list:
                expect_value = read_user_defined_variable()['name']['student_name']
                if stu['studentName'] == expect_value:
                    AssertUtil().assert_body(stu['studentName'], expect_value)
        else:
            lg.error(" ---------- 接口返回信息异常！ ----------")
    with allure.step('提取student_review_id'):
        if res['msg'] == '成功':
            review_list = res['data']
            for i in review_list:
                if i['classId'] == read_extract_yaml()['class_id'] and i['studentName'] == \
                        reviewList_args['request']['body']['studentName']:
                    student_review_id = {"student_review_id": i['reviewId']}
                    write_extract_yaml(student_review_id)
                    lg.info("---------- student_review_id提取成功 ----------")
        else:
            lg.error(" ---------- 接口返回信息异常！ ----------")


queryClassList_args = readApiYaml("../YamlTestCase/teacher_query_classList.yaml").read_testCase_yaml()


@allure.feature('学生入班申请模块')
# @pytest.mark.run(order=4)
@pytest.mark.joinClass
@pytest.mark.parametrize("queryClassList_args", queryClassList_args)
def test_query_class_list(queryClassList_args):
    """老师端审批管理页面查询班级列表"""
    allure.dynamic.story('老师端查询班级列表学生申请')
    allure.dynamic.title(queryClassList_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + queryClassList_args['request']['url']
        method = queryClassList_args['request']['method']
        headers = queryClassList_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = queryClassList_args['request']['body']
        body['schoolId'] = read_extract_yaml()['school_id']
        lg.info("获取的接口请求参数：%s" % queryClassList_args)
        allure.attach(
            json.dumps(queryClassList_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, body, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应参数')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), queryClassList_args['expect']['msg'])
        # school_id = read_extract_yaml()['school_id']
        # sport_teacher = queryClassList_args['expect']['sql']['sportTeacher']
        # sql = "select * from class where school_id='{}' and id='{}'".format(school_id, sport_teacher)
        # db_res = mysql.select_db(sql)
        # db_sportTeacher = db_res[0]['sport_teacher']
        # AssertUtil().assert_db(db_sportTeacher, sport_teacher)


updateReview_args = readApiYaml("../YamlTestCase/teacher_update_studentReviewStatus.yaml").read_testCase_yaml()


@allure.feature('学生入班申请模块')
# @pytest.mark.run(order=4)
@pytest.mark.joinClass
@pytest.mark.parametrize("updateReview_args", updateReview_args)
def test_update_student_reviewStatus(updateReview_args):
    """老师端更新学生申请记录状态为通过，并且通过查询数据库该申请记录，验证通过申请"""
    allure.dynamic.story('老师端更新学生审批状态')
    allure.dynamic.title(updateReview_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + updateReview_args['request']['url']
        method = updateReview_args['request']['method']
        headers = updateReview_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = updateReview_args['request']['body']
        body['reviewIds'] = read_extract_yaml()['student_review_id']
        data = json.dumps(body)
        lg.info("获取的接口请求参数：%s" % updateReview_args)
        allure.attach(
            json.dumps(updateReview_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应参数')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), updateReview_args['expect']['msg'])
        student_review_id = read_extract_yaml()['student_review_id']
        sql = "select * from school_student_review where id ='{}'".format(student_review_id)
        db_res = mysql.select_db(sql)
        db_status = db_res[0]['status']
        expect_value = updateReview_args['expect']['sql']['status']
        AssertUtil().assert_db(db_status, expect_value)


args_all = readApiYaml('../YamlTestCase/web_add_school.yaml').read_testCase_yaml()


@allure.feature('学生入班申请模块')
# @pytest.mark.run(order=12)
@pytest.mark.joinClass
def test_student_review_list():
    """查询学生列表页面，是否存在通过申请的学生"""
    args = args_all['listStudentReview']
    allure.dynamic.story('web管理学生申请列表查询')
    allure.dynamic.title(args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['webHost'] + args['request']['url']
        method = args['request']['method']
        headers = args['request']['headers']
        body = args['request']['body']
        body['reviewTeacher'] = read_user_defined_variable()['name']['teacher_name']
        body['reviewStudent'] = read_user_defined_variable()['name']['student_name']
        res = ru.run_main(method, url, body, headers)
        lg.info("获取的接口请求参数：%s" % args)
        allure.attach(json.dumps(args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        lg.info(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), args['expect']['msg'])
        if res['msg'] == '成功':
            records_list = res['data']['records']
            for i in records_list:
                expect_value = read_user_defined_variable()['name']['student_name']
                if i['reviewId'] == read_extract_yaml()['student_review_id']:
                    studentName = i['studentName']
                    AssertUtil().assert_body(studentName, expect_value)
        else:
            lg.error("---------- 接口返回信息异常！ ----------")


@allure.feature('学生入班申请模块')
# @pytest.mark.run(order=13)
@pytest.mark.joinClass
def test_query_student():
    """查询学生申请列表页面，是否存在学生申请记录"""
    args = args_all['listStudentPage']
    allure.dynamic.story('web管理学生列表查询')
    allure.dynamic.title(args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['webHost'] + args['request']['url']
        method = args['request']['method']
        headers = args['request']['headers']
        body = args['request']['body']
        body['userNameAndMobile'] = read_user_defined_variable()['mobile']['student_mobile']
        res = ru.run_main(method, url, body, headers)
        lg.info("获取的接口请求参数：%s" % args)
        allure.attach(json.dumps(args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        lg.info(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), args['expect']['msg'])
        records_list = res['data']['records']
        for i in records_list:
            schoolName = read_user_defined_variable()['schoolInfo']['school_name']
            if i['userId'] == read_extract_yaml()['student_userId'] and i['schoolName'] == schoolName:
                expect_value = read_user_defined_variable()['name']['student_name']
                studentName = i['realName']
                AssertUtil().assert_db(studentName, expect_value)
            else:
                lg.warning("---------- 接口返回数据内找不到该学生 ----------")
