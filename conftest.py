import pytest

from Common.loguru_util import GetLog
from Common.mysql_util import Mysql
from Common.deal_yaml import readApiYaml, clear_extract_yaml

lg = GetLog()
mysql = Mysql()


@pytest.fixture(scope="session", autouse=True)
def del_schoolName():
    """查询数据库内是否存在用例中的学校，存在则删除"""
    args_all = readApiYaml('../YamlTestCase/web_add_school.yaml').read_testCase_yaml()
    args = args_all['addSchool']
    school_name = args['request']['body']['name']
    sql = "SELECT * FROM school WHERE name='{}'".format(school_name)
    db_res = mysql.select_db(sql)
    if db_res is not None:
        mysql.delete_db("delete from school where name='{}'".format(school_name))
        sql = "SELECT * FROM school WHERE name='{}'".format(school_name)
        if sql is None:
            lg.info("----------该学校名称成功从数据库删除----------")
    else:
        lg.info("----------该学校名称不存在于数据库----------")

    # yield
    # clear_extract_yaml()


