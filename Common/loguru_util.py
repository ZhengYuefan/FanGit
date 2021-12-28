
import os
from configparser import ConfigParser
from time import strftime
from loguru import logger


class GetLog:
    __instance = None
    __init_flag = True

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(GetLog, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        if self.__init_flag:
            # current = strftime('%Y%m%d-%H%M%S')
            cfg = ConfigParser()
            cfg.read('Config/loguru.ini', encoding="utf-8")
            logDir = os.path.expanduser("Report/log")
            logFile = os.path.join(logDir, '{time}.log')
            # 如果日志存放目录不存在，执行新建目录
            if not os.path.exists(logDir):
                os.mkdir(logDir)
            logger.add(logFile,
                       retention=cfg.get('log', 'retention'),
                       rotation=cfg.get('log', 'rotation'),
                       format=cfg.get('log', 'format'),
                       level=cfg.get('log', 'level'),
                       mode="a",
                       encoding="utf-8")  # 初始化配置
            self.__init_flag: False

    def info(self, msg):
        return logger.info(msg)

    def debug(self, msg):
        return logger.debug(msg)

    def warning(self, msg):
        return logger.warning(msg)

    def error(self, msg):
        return logger.error(msg)

    def critical(self, msg):
        return logger.critical(msg)


if __name__ == '__main__':
    log = GetLog()
    for i in range(10):
        log.info("i love you!!!")
        log.debug("i love you!!!")
        log.warning("i love you!!!")
        log.error("i love you!!!")
        log.critical("i love you!!!")
