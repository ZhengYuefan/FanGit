import datetime
import logging

# 设置日志生成路径和名称
logDir = f'../Report/log/小凡日志-{datetime.datetime.now().strftime("%Y%m%d%H%M")}.log'


class Log:
    def __init__(self, level="DEBUG"):
        """日志器"""
        self.log = logging.getLogger("郑岳凡")
        self.log.setLevel(level)

    def get_formatter(self):
        """格式器"""
        # 定义输出格式
        console_fmt = logging.Formatter(
            fmt="%(name)s - %(asctime)s - %(filename)s - %(levelname)s - [line:%(lineno)d] - %(message)s")
        file_fmt = logging.Formatter(fmt="%(name)s - %(asctime)s - %(filename)s - %(levelname)s - %(message)s")
        return console_fmt, file_fmt

    def console_handle(self, level="DEBUG"):
        """控制台处理器"""
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        # 处理器添加格式器
        console_handler.setFormatter(self.get_formatter()[0])
        return console_handler

    def file_handle(self, level="DEBUG"):
        """文件处理器"""
        file_handler = logging.FileHandler(logDir, mode="a", encoding="utf-8")
        file_handler.setLevel(level)
        # 处理器添加格式器
        file_handler.setFormatter(self.get_formatter()[1])
        return file_handler

    def get_log(self):
        """日志器添加控制台处理器和文件处理器"""
        self.log.addHandler(self.console_handle())
        self.log.addHandler(self.file_handle())
        return self.log


# log = Log()
# logger = log.get_log()
# logger.info("info信息")
