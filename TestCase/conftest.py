import pytest

from Common.loguru_util import GetLog
from Common.mysql_util import Mysql
from Common.deal_yaml import readApiYaml

lg = GetLog()
mysql = Mysql()


@pytest.fixture(scope="function", autouse=True)
def my_fixture():
    lg.info("========== 接口测试用例执行开始 ========== ")
    yield
    lg.info("========== 接口测试用例执行结束 ==========\n\n")








