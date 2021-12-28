import json
import allure
import pytest

from Common.request_util import RequestUtil
from Common.assert_util import AssertUtil
from Common.loguru_util import GetLog
from Common.mysql_util import Mysql
from Common.deal_yaml import readApiYaml, read_config_yaml, read_extract_yaml, read_user_defined_variable, write_extract_yaml

lg = GetLog()
ru = RequestUtil()
mysql = Mysql()


sportsList_args = readApiYaml('../YamlTestCase/sports/sports_list.yaml').read_testCase_yaml()
@allure.feature('运动模块')
@allure.story('运动列表--首页')
@pytest.mark.sport
@pytest.mark.parametrize("sportsList_args", sportsList_args)
def test_sports_listSports(sportsList_args):
    """获取运动首页的运动列表"""
    allure.dynamic.title(sportsList_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + sportsList_args['request']['url']
        method = sportsList_args['request']['method']
        headers = sportsList_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        lg.info("获取的接口请求参数：%s" % sportsList_args)
        allure.attach(json.dumps(sportsList_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), sportsList_args['expect']['msg'])


sportsExpectConsumption_args = readApiYaml('../YamlTestCase/sports/sports_expect_consumption.yaml').read_testCase_yaml()
@allure.feature('运动模块')
@allure.story('预计消耗')
@pytest.mark.sport
@pytest.mark.parametrize("sportsExpectConsumption_args", sportsExpectConsumption_args)
def test_sports_expect_consumption(sportsExpectConsumption_args):
    """获取运动首页的运动列表"""
    allure.dynamic.title(sportsExpectConsumption_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + sportsExpectConsumption_args['request']['url']
        method = sportsExpectConsumption_args['request']['method']
        headers = sportsExpectConsumption_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = sportsExpectConsumption_args['request']['body']
        lg.info("获取的接口请求参数：%s" % sportsExpectConsumption_args)
        allure.attach(json.dumps(sportsExpectConsumption_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, body, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), sportsExpectConsumption_args['expect']['msg'])
        AssertUtil().assert_body(res['data']['totalCalories'], sportsExpectConsumption_args['expect']['totalCalories'])


sportsSubmit_args = readApiYaml('../YamlTestCase/sports/sports_submit.yaml').read_testCase_yaml()
@allure.feature('运动模块')
@allure.story('提交运动记录')
@pytest.mark.sport
@pytest.mark.parametrize("sportsSubmit_args", sportsSubmit_args)
def test_sports_submit(sportsSubmit_args):
    """提交运动记录，包括计时、计数、自由模式的跳绳、跑步"""
    allure.dynamic.title(sportsSubmit_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + sportsSubmit_args['request']['url']
        method = sportsSubmit_args['request']['method']
        headers = sportsSubmit_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = sportsSubmit_args['request']['body']
        data = json.dumps(body)
        lg.info("获取的接口参数：%s" % sportsSubmit_args)
        allure.attach(
            json.dumps(sportsSubmit_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), sportsSubmit_args['expect']['msg'])
        record_id = res['data']['recordId']
        sql = "select * from sports_record where id={};".format(record_id)
        db_res = mysql.select_db(sql)
        db_sports_id = db_res[0]['sports_id']
        expect_value = sportsSubmit_args['expect']['sql']['sports_id']
        AssertUtil().assert_body(db_sports_id, expect_value)


sportsRecord_args = readApiYaml('../YamlTestCase/sports/sports_getRecordId.yaml').read_testCase_yaml()
@allure.feature('运动模块')
@allure.story('提交运动，获取运动记录id')
@pytest.mark.sport
@pytest.mark.parametrize("sportsRecord_args", sportsRecord_args)
def test_sports_recordId(sportsRecord_args):
    """提交运动记录，提取响应报文中的recordId"""
    allure.dynamic.title(sportsRecord_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + sportsRecord_args['request']['url']
        method = sportsRecord_args['request']['method']
        headers = sportsRecord_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = sportsRecord_args['request']['body']
        data = json.dumps(body)
        lg.info("获取的接口参数：%s" % sportsRecord_args)
        allure.attach(
            json.dumps(sportsRecord_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
            name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), sportsRecord_args['expect']['msg'])
        record_id = res['data']['recordId']
        sql = "select * from sports_record where id={};".format(record_id)
        db_res = mysql.select_db(sql)
        db_sports_id = db_res[0]['sports_id']
        expect_value = sportsRecord_args['expect']['sql']['sports_id']
        AssertUtil().assert_body(db_sports_id, expect_value)
    with allure.step('提取sport_record_id'):
        if res['msg'] == '成功':
            sport_record_id = {"sport_record_id": res['data']['recordId']}
            write_extract_yaml(sport_record_id)
        else:
            lg.error("---------- 提交运动记录接口请求异常！----------")


sportsResult_args = readApiYaml('../YamlTestCase/sports/sports_result.yaml').read_testCase_yaml()
@allure.feature('运动模块')
@allure.story('运动成绩')
@pytest.mark.sport
@pytest.mark.parametrize("sportsResult_args", sportsResult_args)
def test_sports_result(sportsResult_args):
    """运动结束，运动成绩页面"""
    allure.dynamic.title(sportsResult_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + sportsResult_args['request']['url']
        method = sportsResult_args['request']['method']
        headers = sportsResult_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = sportsResult_args['request']['body']
        body['recordId'] = read_extract_yaml()['sport_record_id']
        lg.info("获取的接口请求参数：%s" % sportsResult_args)
        allure.attach(json.dumps(sportsResult_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, body, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), sportsResult_args['expect']['msg'])
        AssertUtil().assert_body(str(res['data']['realName']), read_user_defined_variable()['name']['teacher_name'])


sportsConsumption_args = readApiYaml('../YamlTestCase/sports/sports_consumption.yaml').read_testCase_yaml()
@allure.feature('运动模块')
@allure.story('运动消耗')
@pytest.mark.sport
@pytest.mark.parametrize("sportsConsumption_args", sportsConsumption_args)
def test_sports_consumption(sportsConsumption_args):
    """运动结束，运动消耗页面"""
    allure.dynamic.title(sportsConsumption_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + sportsConsumption_args['request']['url']
        method = sportsConsumption_args['request']['method']
        headers = sportsConsumption_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = sportsConsumption_args['request']['body']
        body['recordId'] = read_extract_yaml()['sport_record_id']
        lg.info("获取的接口请求参数：%s" % sportsConsumption_args)
        allure.attach(json.dumps(sportsConsumption_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, body, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), sportsConsumption_args['expect']['msg'])


sportsAbility_args = readApiYaml('../YamlTestCase/sports/sports_ability.yaml').read_testCase_yaml()
@allure.feature('运动模块')
@allure.story('运动能力')
@pytest.mark.sport
@pytest.mark.parametrize("sportsAbility_args", sportsAbility_args)
def test_sports_ability(sportsAbility_args):
    """运动结束，运动能力"""
    allure.dynamic.title(sportsAbility_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + sportsAbility_args['request']['url']
        method = sportsAbility_args['request']['method']
        headers = sportsAbility_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = sportsAbility_args['request']['body']
        lg.info("获取的接口请求参数：%s" % sportsAbility_args)
        allure.attach(json.dumps(sportsAbility_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, body, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), sportsAbility_args['expect']['msg'])


sportsVideo_args = readApiYaml('../YamlTestCase/sports/sports_video.yaml').read_testCase_yaml()
@allure.feature('运动模块')
@allure.story('获取运动视频')
@pytest.mark.sport
@pytest.mark.parametrize("sportsVideo_args", sportsVideo_args)
def test_sports_video(sportsVideo_args):
    """获取运动记录视频地址"""
    allure.dynamic.title(sportsVideo_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + sportsVideo_args['request']['url']
        method = sportsVideo_args['request']['method']
        headers = sportsVideo_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = sportsVideo_args['request']['body']
        body['recordId'] = read_extract_yaml()['sport_record_id']
        lg.info("获取的接口请求参数：%s" % sportsVideo_args)
        allure.attach(json.dumps(sportsVideo_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, body, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), sportsVideo_args['expect']['msg'])


sportsDelVideo_args = readApiYaml('../YamlTestCase/sports/sports_del_video.yaml').read_testCase_yaml()
@allure.feature('运动模块')
@allure.story('逻辑删除运动视频记录')
@pytest.mark.sport
@pytest.mark.parametrize("sportsDelVideo_args", sportsDelVideo_args)
def test_sports_del_video(sportsDelVideo_args):
    """逻辑删除运动视频记录"""
    allure.dynamic.title(sportsDelVideo_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + sportsDelVideo_args['request']['url']
        method = sportsDelVideo_args['request']['method']
        headers = sportsDelVideo_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = sportsDelVideo_args['request']['body']
        body['recordId'] = read_extract_yaml()['sport_record_id']
        data = json.dumps(body)
        lg.info("获取的接口请求参数：%s" % sportsDelVideo_args)
        allure.attach(json.dumps(sportsDelVideo_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, data, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), sportsDelVideo_args['expect']['msg'])


sportsMyRecord_args = readApiYaml('../YamlTestCase/sports/sports_mine_record.yaml').read_testCase_yaml()
@allure.feature('运动模块')
@allure.story('我的--运动记录')
@pytest.mark.sport
@pytest.mark.parametrize("sportsMyRecord_args", sportsMyRecord_args)
def test_sports_mine_record(sportsMyRecord_args):
    """我的页面--运动记录"""
    allure.dynamic.title(sportsMyRecord_args['name'])
    with allure.step('发送请求'):
        url = read_config_yaml()['appHost'] + sportsMyRecord_args['request']['url']
        method = sportsMyRecord_args['request']['method']
        headers = sportsMyRecord_args['request']['headers']
        headers['Authorization'] = read_extract_yaml()['teacher_token']
        body = sportsMyRecord_args['request']['body']
        lg.info("获取的接口请求参数：%s" % sportsMyRecord_args)
        allure.attach(json.dumps(sportsMyRecord_args, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口请求参数')
        res = ru.run_main(method, url, body, headers)
        lg.info("返回的接口响应报文：%s" % json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False))
        allure.attach(json.dumps(res, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False),
                      name='接口响应报文')
    with allure.step('断言结果'):
        AssertUtil().assert_body(str(res['msg']), sportsMyRecord_args['expect']['msg'])
        date_day = res['data'][0]['recordId']
        expect_value = read_extract_yaml()['sport_record_id']
        AssertUtil().assert_body(date_day, expect_value)
