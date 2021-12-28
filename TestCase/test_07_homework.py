import json
import allure
import pytest

from Common.loguru_util import GetLog
from Common.request_util import RequestUtil
from Common.assert_util import AssertUtil
from Common.mysql_util import Mysql
from Common.deal_yaml import read_config_yaml, read_extract_yaml, readApiYaml, read_user_defined_variable, write_extract_yaml

lg = GetLog()
ru = RequestUtil()
mysql = Mysql()


addHomework_args = readApiYaml('../YamlTestCase/homework_add.yaml').read_testCase_yaml()
@allure.feature('作业模块')
@allure.story('创建作业')
@pytest.mark.homework
@pytest.mark.parametrize("addHomework_args", addHomework_args)
def test_homework_add(addHomework_args):
    """老师端创建作业"""
    allure.dynamic.title(addHomework_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + addHomework_args['request']['url']
        method = addHomework_args['request']['method']
        headers = addHomework_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = addHomework_args['request']['body']
        body['classId'] = read_extract_yaml()['class_id']
        data = json.dumps(body)
        lg.info("获取的接口请求参数：%s" % addHomework_args)
        allure.attach(json.dumps(addHomework_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        lg.info("获取的接口请求参数：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), addHomework_args['expect']['msg'])
        res_code = res['data']['code']
        expect_value = addHomework_args['expect']['data_code']
        AssertUtil().assert_code(res_code, expect_value)


homeworkTemplate_args = readApiYaml('../YamlTestCase/homework_template.yaml').read_testCase_yaml()
@allure.feature('作业模块')
@allure.story('查看作业模板')
@pytest.mark.homework
@pytest.mark.parametrize("homeworkTemplate_args", homeworkTemplate_args)
def test_homework_template(homeworkTemplate_args):
    """老师端创建作业"""
    allure.dynamic.title(homeworkTemplate_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + homeworkTemplate_args['request']['url']
        method = homeworkTemplate_args['request']['method']
        headers = homeworkTemplate_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = homeworkTemplate_args['request']['body']
        data = json.dumps(body)
        lg.info("获取的接口请求参数：%s" % homeworkTemplate_args)
        allure.attach(json.dumps(homeworkTemplate_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        lg.info("获取的接口请求参数：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), homeworkTemplate_args['expect']['msg'])
    with allure.step('提取homework_id'):
        if res['msg'] == '成功':
            list_data = res['data']
            for i in list_data:
                if i['status'] == 2 and i['statusName'] == '发布':
                    manual_homework_id = {"manual_homework_id": i['homeworkId']}
                    write_extract_yaml(manual_homework_id)
                elif i['status'] == 1 and i['statusName'] == '进行中':
                    automatic_homework_id = {"automatic_homework_id": i['homeworkId']}
                    write_extract_yaml(automatic_homework_id)


homeworkPublish_args = readApiYaml('../YamlTestCase/homework_manualPublish.yaml').read_testCase_yaml()
@allure.feature('作业模块')
@allure.story('老师手动发布作业')
@pytest.mark.homework
@pytest.mark.parametrize("homeworkPublish_args", homeworkPublish_args)
def test_homework_publish(homeworkPublish_args):
    """老师端在作业模板页面，手动点击发布按钮发布作业"""
    allure.dynamic.title(homeworkPublish_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + homeworkPublish_args['request']['url']
        method = homeworkPublish_args['request']['method']
        headers = homeworkPublish_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = homeworkPublish_args['request']['body']
        body['homeworkId'] = read_extract_yaml()['manual_homework_id']
        data = json.dumps(body)
        lg.info("获取的接口请求参数：%s" % homeworkPublish_args)
        allure.attach(json.dumps(homeworkPublish_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        lg.info("获取的接口请求参数：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), homeworkPublish_args['expect']['msg'])
        AssertUtil().assert_body(str(res['data']), homeworkPublish_args['expect']['data'])


homeworkToday_args = readApiYaml('../YamlTestCase/homework_today.yaml').read_testCase_yaml()
@allure.feature('作业模块')
@allure.story('老师端今日作业记录')
@pytest.mark.homework
@pytest.mark.parametrize("homeworkToday_args", homeworkToday_args)
def test_homework_today(homeworkToday_args):
    """老师端查看今日作业记录"""
    allure.dynamic.title(homeworkToday_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + homeworkToday_args['request']['url']
        method = homeworkToday_args['request']['method']
        headers = homeworkToday_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = homeworkToday_args['request']['body']
        body['dateStr'] = str(read_user_defined_variable()['currentDate']['date_day'])
        data = json.dumps(body)
        lg.info("获取的接口请求参数：%s" % homeworkToday_args)
        allure.attach(json.dumps(homeworkToday_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        lg.info("获取的接口请求参数：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), homeworkToday_args['expect']['msg'])
        if res['msg'] == '成功':
            list_data = res['data']
            for i in list_data:
                homework_id = read_extract_yaml()['manual_homework_id']
                if i['homeworkId'] == homework_id:
                    AssertUtil().assert_body(i['homeworkId'], homework_id)
    with allure.step('提取publish_record_id'):
        if res['msg'] == '成功':
            list_data = res['data']
            for i in list_data:
                homework_id = read_extract_yaml()['manual_homework_id']
                if i['homeworkId'] == homework_id:
                    publish_record_id = {"publish_record_id": i['publishRecordId']}
                    write_extract_yaml(publish_record_id)


homeworkDetail_args = readApiYaml('../YamlTestCase/homework_homePage.yaml').read_testCase_yaml()
@allure.feature('作业模块')
@allure.story('学生查看作业，提取homework_taskId')
@pytest.mark.homework
@pytest.mark.parametrize("homeworkDetail_args", homeworkDetail_args)
def test_homework_stu_HMDetail(homeworkDetail_args):
    """学生端查看任务首页，提取作业任务id"""
    allure.dynamic.title(homeworkDetail_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + homeworkDetail_args['request']['url']
        method = homeworkDetail_args['request']['method']
        headers = homeworkDetail_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['student_token']
        lg.info("获取的接口请求参数：%s" % homeworkDetail_args)
        allure.attach(
            json.dumps(homeworkDetail_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), homeworkDetail_args['expect']['msg'])
    with allure.step('提取homework_taskId'):
        if res['msg'] == '成功':
            list_task = res['data']['task']
            expect_value = read_extract_yaml()['manual_homework_id']
            for i in list_task:
                if i['title'] == '体育作业' and i['relationId'] == expect_value:
                    homework_taskId = {"homework_taskId": i['id']}
                    write_extract_yaml(homework_taskId)
                else:
                    pass
        else:
            lg.error("---------- 查看作业完成进度请求异常！ ----------")


homeworkSubmit_args = readApiYaml('../YamlTestCase/homework_submit.yaml').read_testCase_yaml()
@allure.feature('作业模块')
@allure.story('提交作业')
@pytest.mark.homework
@pytest.mark.parametrize("homeworkSubmit_args", homeworkSubmit_args)
def test_homework_submit(homeworkSubmit_args):
    """学生端提交运动记录，执行家庭作业内容"""
    allure.dynamic.title(homeworkSubmit_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + homeworkSubmit_args['request']['url']
        method = homeworkSubmit_args['request']['method']
        headers = homeworkSubmit_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['student_token']
        body = homeworkSubmit_args['request']['body']
        body['taskId'] = read_extract_yaml()['homework_taskId']
        data = json.dumps(body)
        lg.info("获取的接口参数：%s" % homeworkSubmit_args)
        allure.attach(
            json.dumps(homeworkSubmit_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), homeworkSubmit_args['expect']['msg'])
        record_id = res['data']['recordId']
        sql = "select * from sports_record where id={};".format(record_id)
        db_res = mysql.select_db(sql)
        db_sports_id = db_res[0]['sports_id']
        expect_value = homeworkSubmit_args['expect']['sql']['sports_id']
        AssertUtil().assert_body(db_sports_id, expect_value)


homeworkSpeed_args = readApiYaml('../YamlTestCase/homework_homePage.yaml').read_testCase_yaml()
@allure.feature('作业模块')
@allure.story('查看作业完成进度')
@pytest.mark.homework
@pytest.mark.parametrize("homeworkSpeed_args", homeworkSpeed_args)
def test_homework_speed(homeworkSpeed_args):
    """学生端查看任务首页，验证提交运动记录后作业完成进度是否大于0%"""
    allure.dynamic.title(homeworkSpeed_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + homeworkSpeed_args['request']['url']
        method = homeworkSpeed_args['request']['method']
        headers = homeworkSpeed_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['student_token']
        lg.info("获取的接口请求参数：%s" % homeworkSpeed_args)
        allure.attach(
            json.dumps(homeworkSpeed_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), homeworkSpeed_args['expect']['msg'])
        if res['msg'] == '成功':
            list_task = res['data']['task']
            expect_value = read_extract_yaml()['manual_homework_id']
            for i in list_task:
                if i['title'] == '体育作业' and i['relationId'] == expect_value:
                    AssertUtil().assert_body(i['relationId'], expect_value)
                    if i['speed'] != 0:
                        lg.info("---------- 运动计划进度大于0，恭喜！ ----------")
                    else:
                        lg.warning("---------- 运动计划进度还是0！ ----------")
                else:
                    pass
        else:
            lg.error("---------- 查看作业完成进度请求异常！ ----------")


homeworkHistory_args = readApiYaml('../YamlTestCase/homework_history.yaml').read_testCase_yaml()
@allure.feature('作业模块')
@allure.story('历史作业记录')
@pytest.mark.homework
@pytest.mark.parametrize("homeworkHistory_args", homeworkHistory_args)
def test_homework_history(homeworkHistory_args):
    """老师端作业历史记录"""
    allure.dynamic.title(homeworkHistory_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + homeworkHistory_args['request']['url']
        method = homeworkHistory_args['request']['method']
        headers = homeworkHistory_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = homeworkHistory_args['request']['body']
        data = json.dumps(body)
        lg.info("获取的接口参数：%s" % homeworkHistory_args)
        allure.attach(
            json.dumps(homeworkHistory_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), homeworkHistory_args['expect']['msg'])
        if res['msg'] == '成功':
            list_homework = res['data']
            for i in list_homework:
                homeworkId = read_extract_yaml()['manual_homework_id']
                if i['homeworkId'] == homeworkId:
                    AssertUtil().assert_body(i['homeworkId'], homeworkId)
        else:
            lg.error("---------- 查看历史作业记录请求异常！ ----------")


homeworkSelection_args = readApiYaml('../YamlTestCase/homework_selectionCondition.yaml').read_testCase_yaml()
@allure.feature('作业模块')
@allure.story('作业选择条件')
@pytest.mark.homework
@pytest.mark.parametrize("homeworkSelection_args", homeworkSelection_args)
def test_homework_selection_condition(homeworkSelection_args):
    """老师端创建作业页面的作业选择条件"""
    allure.dynamic.title(homeworkSelection_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + homeworkSelection_args['request']['url']
        method = homeworkSelection_args['request']['method']
        headers = homeworkSelection_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        lg.info("获取的接口参数：%s" % homeworkSelection_args)
        allure.attach(
            json.dumps(homeworkSelection_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), homeworkSelection_args['expect']['msg'])


homeworkStuDetail_args = readApiYaml('../YamlTestCase/homework_stu_homeworkDetail.yaml').read_testCase_yaml()
@allure.feature('作业模块')
@allure.story('学生作业记录详情')
@pytest.mark.homework
@pytest.mark.parametrize("homeworkStuDetail_args", homeworkStuDetail_args)
def test_homework_stu_homeworkDetail(homeworkStuDetail_args):
    """学生端查看作业记录详情"""
    allure.dynamic.title(homeworkStuDetail_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + homeworkStuDetail_args['request']['url']
        method = homeworkStuDetail_args['request']['method']
        headers = homeworkStuDetail_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['student_token']
        body = homeworkStuDetail_args['request']['body']
        body['taskId'] = read_extract_yaml()['homework_taskId']
        lg.info("获取的接口参数：%s" % homeworkStuDetail_args)
        allure.attach(
            json.dumps(homeworkStuDetail_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, body, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), homeworkStuDetail_args['expect']['msg'])


homeworkMyClass_args = readApiYaml('../YamlTestCase/homework_myClass.yaml').read_testCase_yaml()
@allure.feature('作业模块')
@allure.story('作业记录-我的班级--老师端')
@pytest.mark.homework
@pytest.mark.parametrize("homeworkMyClass_args", homeworkMyClass_args)
def test_homework_teacher_myClass(homeworkMyClass_args):
    """老师端作业记录--我的班级"""
    allure.dynamic.title(homeworkMyClass_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + homeworkMyClass_args['request']['url']
        method = homeworkMyClass_args['request']['method']
        headers = homeworkMyClass_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = homeworkMyClass_args['request']['body']
        body['homeworkId'] = read_extract_yaml()['publish_record_id']
        body['dateStr'] = str(read_user_defined_variable()['currentDate']['date_day'])
        lg.info("获取的接口参数：%s" % homeworkMyClass_args)
        allure.attach(
            json.dumps(homeworkMyClass_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, body, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), homeworkMyClass_args['expect']['msg'])


homeworkClassDetail_args = readApiYaml('../YamlTestCase/homework_class_detail.yaml').read_testCase_yaml()
@allure.feature('作业模块')
@allure.story('班级作业详情')
@pytest.mark.homework
@pytest.mark.parametrize("homeworkClassDetail_args", homeworkClassDetail_args)
def test_homework_class_detail(homeworkClassDetail_args):
    """老师端班级作业详情"""
    allure.dynamic.title(homeworkClassDetail_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + homeworkClassDetail_args['request']['url']
        method = homeworkClassDetail_args['request']['method']
        headers = homeworkClassDetail_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = homeworkClassDetail_args['request']['body']
        body['classId'] = read_extract_yaml()['class_id']
        body['dateStr'] = str(read_user_defined_variable()['currentDate']['date_day'])
        body['relationId'] = read_extract_yaml()['publish_record_id']
        lg.info("获取的接口参数：%s" % homeworkClassDetail_args)
        allure.attach(
            json.dumps(homeworkClassDetail_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, body, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), homeworkClassDetail_args['expect']['msg'])
        if res['msg'] == '成功':
            list_stu = res['data']['list']
            for i in list_stu:
                stu_name = read_user_defined_variable()['name']['student_name']
                realName = i['realName']
                if realName == stu_name:
                    AssertUtil().assert_body(realName, stu_name)
        else:
            lg.error("---------- 查看班级作业详情请求异常！ ----------")


homeworkStu_args = readApiYaml('../YamlTestCase/homework_stu_detail.yaml').read_testCase_yaml()
@allure.feature('作业模块')
@allure.story('老师查看学生作业详情')
@pytest.mark.homework
@pytest.mark.parametrize("homeworkStu_args", homeworkStu_args)
def test_homework_stu_detail(homeworkStu_args):
    """老师端班级页面，查看学生作业详情"""
    allure.dynamic.title(homeworkStu_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + homeworkStu_args['request']['url']
        method = homeworkStu_args['request']['method']
        headers = homeworkStu_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = homeworkStu_args['request']['body']
        body['userId'] = read_extract_yaml()['student_userId']
        data = json.dumps(body)
        lg.info("获取的接口参数：%s" % homeworkStu_args)
        allure.attach(
            json.dumps(homeworkStu_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), homeworkStu_args['expect']['msg'])
        if res['msg'] == '成功':
            list_data = res['data']
            for i in list_data:
                homeworkId = read_extract_yaml()['manual_homework_id']
                relationId = i['relationId']
                if relationId == homeworkId:
                    AssertUtil().assert_body(relationId, homeworkId)
        else:
            lg.error("---------- 查看学生作业详情请求异常！ ----------")


homework_del_template_args = readApiYaml('../YamlTestCase/homework_del_template.yaml').read_testCase_yaml()
@allure.feature('作业模块')
@allure.story('删除作业模板')
@pytest.mark.homework
@pytest.mark.parametrize("homework_del_template_args", homework_del_template_args)
def test_homework_del_template(homework_del_template_args):
    """老师端班级页面，查看学生作业详情"""
    allure.dynamic.title(homework_del_template_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + homework_del_template_args['request']['url']
        method = homework_del_template_args['request']['method']
        headers = homework_del_template_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = homework_del_template_args['request']['body']
        body['homeworkId'] = read_extract_yaml()['automatic_homework_id']
        lg.info("获取的接口参数：%s" % homework_del_template_args)
        allure.attach(
            json.dumps(homework_del_template_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, body, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), homework_del_template_args['expect']['msg'])
        AssertUtil().assert_body(str(res['data']), homework_del_template_args['expect']['data'])

