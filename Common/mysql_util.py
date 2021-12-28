import pymysql
from Common.deal_yaml import read_config_yaml
from Common.loguru_util import GetLog

lg = GetLog()
db_info = read_config_yaml()


class Mysql:
    """初始化数据，连接数据库，光标对象"""

    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host=db_info['database']['db_host'],
                port=db_info['database']['db_port'],
                user=db_info['database']['db_user'],
                password=db_info['database']['db_password'],
                database=db_info['database']['db_name'],
                charset=db_info['database']['db_charset'],
                autocommit=True)
            # 设置数据库返回数据为字典类型
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        except pymysql.Error as e:
            print('数据库连接失败，原因%d：%s' % e)
            lg.error("数据库连接失败，原因%d：%s" % e)

    def __del__(self):
        """对象资源被释放时触发，在对象即将被删除时的最后操作"""
        self.cursor.close()
        self.conn.close()

    def fetch_one(self, sql):
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchone()
        except pymysql.Error as e:
            print("查询失败，原因是：%s" % e)
            lg.error("查询失败，原因是：%s" % e)

    def fetch_all(self, sql):
        try:
            self.cursor.execute(sql)
            # self.conn.commit()
            db_res = self.cursor.fetchall()
            self.conn.commit()
            return db_res
        except pymysql.Error as e:
            print("查询失败，原因是：%s" % e)
            lg.error("查询失败，原因是：%s" % e)

    def select_db(self, sql):
        # self.conn.ping(reconnect=True)
        try:
            self.cursor.execute(sql)
            # self.conn.commit()
            db_res = self.cursor.fetchall()
            return db_res
        except pymysql.Error as e:
            print('数据库连接失败，原因%s' % e)
            lg.error("查询失败，原因是：%s" % e)

    def insert_db(self, sql):
        self.conn.ping(reconnect=True)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            # 发生错误时回滚，即撤销刚刚执行的sql语句
            self.conn.rollback()
            print('数据库连接失败，原因%s' % e)
            lg.error("查询失败，原因是：%s" % e)

    def delete_db(self, sql):
        try:
            self.cursor.execute(sql)
            # self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print('数据库连接失败，原因%s' % e)
            lg.error("查询失败，原因是：%s" % e)

    def update_db(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print('数据库连接失败，原因%s' % e)
            lg.error("查询失败，原因是：%s" % e)


if __name__ == '__main__':
    from Common.deal_yaml import read_config_yaml, write_extract_yaml, readApiYaml
    from Common.assert_util import AssertUtil

    args_all = readApiYaml('../YamlTestCase/web_add_school.yaml').read_testCase_yaml()
    args = args_all['addSchool']
    school_name = args['request']['body']['name']
    mysql = Mysql()
    # sql2 = "DELETE FROM school WHERE name='{}'".format(school_name)
    # w = mysql.delete_db(sql2)
    # sql3 = "insert into school (id, type, delete_flag, name, address) values (189, 0, 0, 'Test测试学院', '聚光中心');"
    # de = mysql.insert_db(sql3)
    sql = "select * from school where name='{}'".format(school_name)
    res = mysql.fetch_all(sql)
    #print(w)
    # print(de)
    print(res)