import json
import pytest
import allure

from Common.deal_yaml import readApiYaml, read_extract_yaml, read_config_yaml, write_extract_yaml, \
    read_user_defined_variable
from Common.request_util import RequestUtil
from Common.loguru_util import GetLog
from Common.assert_util import AssertUtil
from Common.mysql_util import Mysql

ru = RequestUtil()
lg = GetLog()
mysql = Mysql()

addDailyGoals_args = readApiYaml('../YamlTestCase/task_add_dailyGoals.yaml').read_testCase_yaml()


@allure.feature('每日目标模块')
@allure.story('学生端创建每日目标')
@pytest.mark.dailyGoals
@pytest.mark.parametrize("addDailyGoals_args", addDailyGoals_args)
def test_add_daily_goals(addDailyGoals_args):
    """学生端创建每日目标，内容为：跳绳100个"""
    allure.dynamic.title(addDailyGoals_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + addDailyGoals_args['request']['url']
        method = addDailyGoals_args['request']['method']
        headers = addDailyGoals_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['student_token']
        body = addDailyGoals_args['request']['body']
        data = json.dumps(body)
        lg.info("获取的接口请求参数：%s" % addDailyGoals_args)
        allure.attach(
            json.dumps(addDailyGoals_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), addDailyGoals_args['expect']['msg'])
        student_userId = read_extract_yaml()['student_userId']
        sql = "select * from homework_task_day_target where user_id={};".format(student_userId)
        db_res = mysql.select_db(sql)
        for i in db_res:
            if i['sport_name'] == addDailyGoals_args['expect']['sql']['sportName']:
                sportName = i['sport_name']
                expect_value = addDailyGoals_args['expect']['sql']['sportName']
                AssertUtil().assert_body(sportName, expect_value)


listTask_args = readApiYaml('../YamlTestCase/task_homePage.yaml').read_testCase_yaml()


@allure.feature('每日目标模块')
@allure.story('学生端查看任务首页每日目标')
@pytest.mark.dailyGoals
@pytest.mark.parametrize("listTask_args", listTask_args)
def test_query_task_homePage(listTask_args):
    """学生端查看任务首页是否存在创建的每日目标"""
    allure.dynamic.title(listTask_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + listTask_args['request']['url']
        method = listTask_args['request']['method']
        headers = listTask_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['student_token']
        lg.info("获取的接口请求参数：%s" % listTask_args)
        allure.attach(
            json.dumps(listTask_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), listTask_args['expect']['msg'])
        list_task = res['data']['task']
        expect_value = listTask_args['expect']['taskName']
        if res['msg'] == '成功':
            for i in list_task:
                if 'taskName' in dict(i).keys():
                    if i['taskName'] == expect_value:
                        AssertUtil().assert_body(i['taskName'], expect_value)
                else:
                    pass


listTaskByMonth_args = readApiYaml('../YamlTestCase/task_query_listTaskByMonth.yaml').read_testCase_yaml()


@allure.feature('每日目标模块')
@allure.story('学生端查询当前月份有任务的日期')
@pytest.mark.dailyGoals
@pytest.mark.parametrize("listTaskByMonth_args", listTaskByMonth_args)
def test_query_task_by_month(listTaskByMonth_args):
    """学生端查看日程表当前月份有任务的日期"""
    allure.dynamic.title(listTaskByMonth_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + listTaskByMonth_args['request']['url']
        method = listTaskByMonth_args['request']['method']
        headers = listTaskByMonth_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['student_token']
        body = listTaskByMonth_args['request']['body']
        body['date'] = read_user_defined_variable()['currentDate']['date_month']
        lg.info("获取的接口请求参数：%s" % listTaskByMonth_args)
        allure.attach(
            json.dumps(listTaskByMonth_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, body, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), listTaskByMonth_args['expect']['msg'])
        res_date = res['data'][0]
        expect_date = str(read_user_defined_variable()['currentDate']['date_day'])
        AssertUtil().assert_body(res_date, expect_date)


listTaskByDay_args = readApiYaml('../YamlTestCase/task_query_listTaskByDay.yaml').read_testCase_yaml()


@allure.feature('每日目标模块')
@allure.story('学生端查询当前日期的每日目标')
@pytest.mark.dailyGoals
@pytest.mark.parametrize("listTaskByDay_args", listTaskByDay_args)
def test_query_task_by_day(listTaskByDay_args):
    """学生端查询日程表当前日期的任务目标"""
    allure.dynamic.title(listTaskByDay_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + listTaskByDay_args['request']['url']
        method = listTaskByDay_args['request']['method']
        headers = listTaskByDay_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['student_token']
        body = listTaskByDay_args['request']['body']
        body['date'] = str(read_user_defined_variable()['currentDate']['date_day'])
        lg.info("获取的接口请求参数：%s" % listTaskByDay_args)
        allure.attach(
            json.dumps(listTaskByDay_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, body, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), listTaskByDay_args['expect']['msg'])
    with allure.step('提取task_id'):
        if res['msg'] == '成功':
            list_dayTask = res['data']
            for i in list_dayTask:
                if i['title'] == "每日目标-跳绳":
                    jumpRope_taskId = {"jumpRope_taskId": i['id']}
                    write_extract_yaml(jumpRope_taskId)
                elif i['title'] == "每日目标-跑步":
                    running_taskId = {"running_taskId": i['id']}
                    write_extract_yaml(running_taskId)
                elif i['title'] == "每日目标-卡路里":
                    calorie_taskId = {"calorie_taskId": i['id']}
                    write_extract_yaml(calorie_taskId)
                else:
                    pass
        else:
            lg.error("---------- 学生端查看当前日期的每日目标请求异常！ ----------")


mineTaskRecord_args = readApiYaml('../YamlTestCase/task_mine_taskRecord.yaml').read_testCase_yaml()


@allure.feature('每日目标模块')
@allure.story('我的_任务记录')
@pytest.mark.dailyGoals
@pytest.mark.parametrize("mineTaskRecord_args", mineTaskRecord_args)
def test_mine_task_record(mineTaskRecord_args):
    """学生端查看我的->任务记录，每日目标为跳绳的任务"""
    allure.dynamic.title(mineTaskRecord_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + mineTaskRecord_args['request']['url']
        method = mineTaskRecord_args['request']['method']
        headers = mineTaskRecord_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['student_token']
        body = mineTaskRecord_args['request']['body']
        data = json.dumps(body)
        lg.info("获取的接口参数：%s" % mineTaskRecord_args)
        allure.attach(
            json.dumps(mineTaskRecord_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), mineTaskRecord_args['expect']['msg'])
        if res['msg'] == '成功':
            list_taskRecord = res['data']
            for i in list_taskRecord:
                if i['title'] == "每日目标":
                    date_day = read_user_defined_variable()['currentDate']['date_day']
                    if i['createTime'] == 'date_day':
                        AssertUtil().assert_body(i['createTime'], date_day)
                else:
                    pass
        else:
            lg.error("---------- 学生端我的->任务记录请求异常！ ----------")


fulfilTask_args = readApiYaml('../YamlTestCase/task_fulfilTask.yaml').read_testCase_yaml()


@allure.feature('每日目标模块')
@allure.story('完成每日目标运动')
@pytest.mark.dailyGoals
@pytest.mark.parametrize("fulfilTask_args", fulfilTask_args)
def test_fulfil_task(fulfilTask_args):
    """学生端提交运动记录，执行每日目标的任务"""
    allure.dynamic.title(fulfilTask_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + fulfilTask_args['request']['url']
        method = fulfilTask_args['request']['method']
        headers = fulfilTask_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['student_token']
        body = fulfilTask_args['request']['body']
        data = json.dumps(body)
        lg.info("获取的接口参数：%s" % fulfilTask_args)
        allure.attach(
            json.dumps(fulfilTask_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), fulfilTask_args['expect']['msg'])
        record_id = res['data']['recordId']
        sql = "select * from sports_record where id={};".format(record_id)
        db_res = mysql.select_db(sql)
        db_sports_id = db_res[0]['sports_id']
        expect_value = fulfilTask_args['expect']['sql']['sports_id']
        AssertUtil().assert_body(db_sports_id, expect_value)


queryTaskSpeed_args = readApiYaml('../YamlTestCase/task_homePage.yaml').read_testCase_yaml()


@allure.feature('每日目标模块')
@allure.story('查看任务完成进度')
@allure.title('查看任务首页的每日目标完成进度')
@pytest.mark.dailyGoals
@pytest.mark.parametrize("queryTaskSpeed_args", queryTaskSpeed_args)
def test_query_task_speed(queryTaskSpeed_args):
    """学生端再次查看任务首页，验证提交运动记录后是否跳绳、跑步、卡路里全部完成进度都是100%"""
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + queryTaskSpeed_args['request']['url']
        method = queryTaskSpeed_args['request']['method']
        headers = queryTaskSpeed_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['student_token']
        lg.info("获取的接口请求参数：%s" % queryTaskSpeed_args)
        allure.attach(
            json.dumps(queryTaskSpeed_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), queryTaskSpeed_args['expect']['msg'])
        if res['msg'] == '成功':
            list_task = res['data']['task']
            taskName = queryTaskSpeed_args['expect']['taskName']
            for i in list_task:
                if 'taskName' in dict(i).keys():
                    if i['taskName'] == taskName and i['status'] == '3':
                        speed = i['speed']
                        expect_value = str(queryTaskSpeed_args['expect']['fulfilSpeed'])
                        AssertUtil().assert_body(speed, expect_value)
                        lg.info("---------- 每日目标%s已完成，恭喜！ ----------" % queryTaskSpeed_args['expect']['taskName'])
                else:
                    pass
