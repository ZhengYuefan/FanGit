import json
from Common.loguru_util import GetLog


class AssertUtil:
    def __init__(self):
        self.log = GetLog()

    def assert_code(self, code, expected_code):
        """验证接口返回状态码"""
        try:
            assert int(code) == int(expected_code)
            return True
        except:
            self.log.error("code error, code is %s, expected_code is %s" % (code, expected_code))
            raise

    def assert_body(self, body, expected_body):
        """验证返回结果内容相等"""
        try:
            assert body == expected_body
            return True
        except:
            self.log.error("body 错误, body is %s, expected_body is %s" % (body, expected_body))
            raise

    def assert_in_body(self, body, expected_body):
        """验证返回结果是否包含期望的结果"""
        try:
            body = json.dumps(body)
            print(body)
            assert expected_body in body
            return True
        except:
            self.log.error("不包含或者body错误， body is %s, expected_body is %s" % (body, expected_body))
            raise

    def assert_db(self, db_res, expected_value):
        try:
            assert db_res == expected_value
            return True
        except:
            # print("db_res与expected_value不等，db_res is %s, expected_value is %s" % (db_res, expected_value))
            self.log.error("db_res与expected_value不等，db_res is %s, expected_value is %s" % (db_res, expected_value))


if __name__ == '__main__':
    a = AssertUtil()
    a.assert_body("11发热", "11发热")