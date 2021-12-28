import json
import pytest
import allure

from Common.mysql_util import Mysql
from Common.assert_util import AssertUtil
from Common.loguru_util import GetLog
from Common.request_util import RequestUtil
from Common.deal_yaml import readApiYaml, read_extract_yaml, read_config_yaml, read_user_defined_variable, \
    write_extract_yaml

mysql = Mysql()
lg = GetLog()
ru = RequestUtil()

addPlan_args = readApiYaml('../YamlTestCase/plan_addPlan.yaml').read_testCase_yaml()


@allure.feature('任务计划模块')
@allure.story('创建计划')
@pytest.mark.plan
@pytest.mark.parametrize("addPlan_args", addPlan_args)
def test_plan_add(addPlan_args):
    """创建任务计划： 提升成绩"""
    allure.dynamic.title(addPlan_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + addPlan_args['request']['url']
        method = addPlan_args['request']['method']
        headers = addPlan_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = addPlan_args['request']['body']
        data = json.dumps(body)
        lg.info("获取的接口请求参数：%s" % addPlan_args)
        allure.attach(json.dumps(addPlan_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), addPlan_args['expect']['msg'])
        plan_id = res['data']['planId']
        sql = "select * from homework_plan_info where id={}".format(plan_id)
        db_res = mysql.select_db(sql)
        db_motionTarget = db_res[0]['motion_target']
        expect_value = addPlan_args['expect']['sql']['motionTarget']
        AssertUtil().assert_body(db_motionTarget, expect_value)
    with allure.step('提取plan_id'):
        if res['msg'] == '成功':
            plan_id = {"plan_id": res['data']['planId']}
            write_extract_yaml(plan_id)
            lg.info("---------- 提取plan_id成功 ----------")
        else:
            lg.error("---------- 创建新任务计划失败！ ----------")


planRecord_args = readApiYaml('../YamlTestCase/plan_planRecord.yaml').read_testCase_yaml()


@allure.feature('任务计划模块')
@allure.story('计划记录列表')
@pytest.mark.plan
@pytest.mark.parametrize("planRecord_args", planRecord_args)
def test_plan_recordList(planRecord_args):
    """查看计划记录页面列表中是否存在本次创建的任务计划"""
    allure.dynamic.title(planRecord_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + planRecord_args['request']['url']
        method = planRecord_args['request']['method']
        headers = planRecord_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        lg.info("获取的接口请求参数：%s" % planRecord_args)
        allure.attach(json.dumps(planRecord_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), planRecord_args['expect']['msg'])
        if res['msg'] == '成功':
            list_plan = res['data']
            for i in list_plan:
                res_planId = i['id']
                plan_id = read_extract_yaml()['plan_id']
                if res_planId == plan_id:
                    AssertUtil().assert_body(res_planId, plan_id)
                else:
                    lg.error("---------- 未查询到本次创建的计划记录 ----------")
        else:
            lg.error("---------- 计划记录接口请求异常！ ----------")


planInfo_args = readApiYaml('../YamlTestCase/plan_planInfo.yaml').read_testCase_yaml()


@allure.feature('任务计划模块')
@allure.story('根据计划id获取计划信息')
@pytest.mark.plan
@pytest.mark.parametrize("planInfo_args", planInfo_args)
def test_plan_get_planInfo(planInfo_args):
    """根据计划id获取计划信息，提取计划中单个计划的id和title"""
    allure.dynamic.title(planInfo_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + planInfo_args['request']['url']
        method = planInfo_args['request']['method']
        headers = planInfo_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = planInfo_args['request']['body']
        body['planId'] = read_extract_yaml()['plan_id']
        lg.info("获取的接口请求参数：%s" % planInfo_args)
        allure.attach(json.dumps(planInfo_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, body, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), planInfo_args['expect']['msg'])
        res_motionTarget = res['data']['motionTarget']
        expect_value = planInfo_args['expect']['motionTarget']
        AssertUtil().assert_body(res_motionTarget, expect_value)
    with allure.step('提取single_plan_id和对应title'):
        if res['msg'] == '成功':
            single_plan_id_01 = {"single_plan_id_01": res['data']['weekList'][0]['weekOfList'][0]['id']}
            write_extract_yaml(single_plan_id_01)
            single_plan_id_02 = {"single_plan_id_02": res['data']['weekList'][0]['weekOfList'][1]['id']}
            write_extract_yaml(single_plan_id_02)
            single_plan_id_01_title = {"single_plan_id_01_title": res['data']['weekList'][0]['weekOfList'][0]['title']}
            write_extract_yaml(single_plan_id_01_title)
            single_plan_id_02_title = {"single_plan_id_02_title": res['data']['weekList'][0]['weekOfList'][1]['title']}
            write_extract_yaml(single_plan_id_02_title)
        else:
            lg.error("---------- 根据planId获取计划信息请求失败！----------")


planCondition_args = readApiYaml('../YamlTestCase/plan_selection_planConditions.yaml').read_testCase_yaml()


@allure.feature('任务计划模块')
@allure.story('计划选择条件')
@pytest.mark.plan
@pytest.mark.parametrize("planCondition_args", planCondition_args)
def test_plan_selection_criteria(planCondition_args):
    """创建计划时的计划选择条件是接口返回的"""
    allure.dynamic.title(planCondition_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + planCondition_args['request']['url']
        method = planCondition_args['request']['method']
        headers = planCondition_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        lg.info("获取的接口请求参数：%s" % planCondition_args)
        allure.attach(
            json.dumps(planCondition_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), planCondition_args['expect']['msg'])


planDetail_args = readApiYaml('../YamlTestCase/plan_today_planDetail.yaml').read_testCase_yaml()


@allure.feature('任务计划模块')
@allure.story('今日计划详情')
@pytest.mark.plan
@pytest.mark.parametrize("planDetail_args", planDetail_args)
def test_plan_today_planInfo(planDetail_args):
    """创建计划时的计划选择条件是接口返回的"""
    allure.dynamic.title(planDetail_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + planDetail_args['request']['url']
        method = planDetail_args['request']['method']
        headers = planDetail_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = planDetail_args['request']['body']
        body['planId'] = read_extract_yaml()['plan_id']
        body['dateStr'] = str(read_user_defined_variable()['currentDate']['date_day'])
        lg.info("获取的接口请求参数：%s" % planDetail_args)
        allure.attach(
            json.dumps(planDetail_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, body, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), planDetail_args['expect']['msg'])
        res_title = res['data']['title']
        expect_value = planDetail_args['expect']['title']
        AssertUtil().assert_body(res_title, expect_value)


planExchangeOrder_args = readApiYaml('../YamlTestCase/plan_ExchangeOrder.yaml').read_testCase_yaml()


@allure.feature('任务计划模块')
@allure.story('调换计划顺序')
@pytest.mark.plan
@pytest.mark.parametrize("planExchangeOrder_args", planExchangeOrder_args)
def test_plan_change_order(planExchangeOrder_args):
    """老师端调整运动计划的顺序"""
    allure.dynamic.title(planExchangeOrder_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + planExchangeOrder_args['request']['url']
        method = planExchangeOrder_args['request']['method']
        headers = planExchangeOrder_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = planExchangeOrder_args['request']['body']
        body['list'][0]['id'] = read_extract_yaml()['single_plan_id_01']
        body['list'][0]['title'] = read_extract_yaml()['single_plan_id_01_title']
        body['list'][1]['id'] = read_extract_yaml()['single_plan_id_02']
        body['list'][1]['title'] = read_extract_yaml()['single_plan_id_02_title']
        data = json.dumps(body)
        lg.info("获取的接口参数：%s" % planExchangeOrder_args)
        allure.attach(
            json.dumps(planExchangeOrder_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), planExchangeOrder_args['expect']['msg'])
        AssertUtil().assert_body(str(res['data']), planExchangeOrder_args['expect']['data'])


planExecute_args = readApiYaml('../YamlTestCase/plan_execute.yaml').read_testCase_yaml()


@allure.feature('任务计划模块')
@allure.story('执行运动计划')
@pytest.mark.plan
@pytest.mark.parametrize("planExecute_args", planExecute_args)
def test_plan_execute(planExecute_args):
    """老师端提交运动记录，执行每日目标的任务"""
    allure.dynamic.title(planExecute_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + planExecute_args['request']['url']
        method = planExecute_args['request']['method']
        headers = planExecute_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = planExecute_args['request']['body']
        data = json.dumps(body)
        lg.info("获取的接口参数：%s" % planExecute_args)
        allure.attach(
            json.dumps(planExecute_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), planExecute_args['expect']['msg'])
        record_id = res['data']['recordId']
        sql = "select * from sports_record where id={};".format(record_id)
        db_res = mysql.select_db(sql)
        db_sports_id = db_res[0]['sports_id']
        expect_value = planExecute_args['expect']['sql']['sports_id']
        AssertUtil().assert_body(db_sports_id, expect_value)


planSpeed_args = readApiYaml('../YamlTestCase/plan_homePage.yaml').read_testCase_yaml()


@allure.feature('任务计划模块')
@allure.story('查看计划完成进度')
@allure.title('查看任务首页的计划完成进度')
@pytest.mark.plan
@pytest.mark.parametrize("planSpeed_args", planSpeed_args)
def test_query_plan_speed(planSpeed_args):
    """老师端再次查看任务首页，验证提交运动记录后运动计划完成进度是否大于0%"""
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + planSpeed_args['request']['url']
        method = planSpeed_args['request']['method']
        headers = planSpeed_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        lg.info("获取的接口请求参数：%s" % planSpeed_args)
        allure.attach(
            json.dumps(planSpeed_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), planSpeed_args['expect']['msg'])
        if res['msg'] == '成功':
            list_task = res['data']['task']
            expect_value = read_extract_yaml()['plan_id']
            for i in list_task:
                if i['title'] == '计划目标':
                    AssertUtil().assert_body(i['relationId'], expect_value)
                    if i['speed'] != 0:
                        lg.info("---------- 运动计划进度大于0，恭喜！ ----------")
                    else:
                        lg.warning("---------- 运动计划进度还是0！ ----------")
                else:
                    pass
        else:
            lg.error("---------- 查看任务首页计划进度请求异常！ ----------")


planTermination_args = readApiYaml('../YamlTestCase/plan_termination.yaml').read_testCase_yaml()


@allure.feature('任务计划模块')
@allure.story('终止计划')
@pytest.mark.plan
@pytest.mark.parametrize("planTermination_args", planTermination_args)
def test_plan_termination(planTermination_args):
    """老师端手动终止进行中的"""
    allure.dynamic.title(planTermination_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + planTermination_args['request']['url']
        method = planTermination_args['request']['method']
        headers = planTermination_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = planTermination_args['request']['body']
        body['planId'] = str(read_extract_yaml()['plan_id'])
        lg.info("获取的接口请求参数：%s" % planTermination_args)
        allure.attach(
            json.dumps(planTermination_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, body, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), planTermination_args['expect']['msg'])
        plan_id = read_extract_yaml()['plan_id']
        sql = "select * from homework_plan_info where id={};".format(plan_id)
        db_res = mysql.select_db(sql)
        db_deleteFlag = db_res[0]['status']
        expect_value = planTermination_args['expect']['sql']['status']
        AssertUtil().assert_db(db_deleteFlag, expect_value)


planEndDetail_args = readApiYaml('../YamlTestCase/plan_endDetail.yaml').read_testCase_yaml()


@allure.feature('任务计划模块')
@allure.story('计划结束详情')
@pytest.mark.plan
@pytest.mark.parametrize("planEndDetail_args", planEndDetail_args)
def test_plan_endDetail(planEndDetail_args):
    """老师端查看计划结束详情页面"""
    allure.dynamic.title(planEndDetail_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + planEndDetail_args['request']['url']
        method = planEndDetail_args['request']['method']
        headers = planEndDetail_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = planEndDetail_args['request']['body']
        body['planId'] = read_extract_yaml()['plan_id']
        lg.info("获取的接口请求参数：%s" % planEndDetail_args)
        allure.attach(
            json.dumps(planEndDetail_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, body, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), planEndDetail_args['expect']['msg'])
        res_title = res['data']['title']
        expect_value = planEndDetail_args['expect']['title']
        AssertUtil().assert_body(res_title, expect_value)