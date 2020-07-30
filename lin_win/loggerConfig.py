#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/21 0021 20:52
# @Author  : augus
# @FileName: loggerConfig.py
# @Software: PyCharm
import logging.handlers,os
from readConfig import readConfig
rc  = readConfig()
class Logger(logging.Logger):
    def __init__(self, filename=None):
        super(Logger, self).__init__(self)
        # 日志文件名
        if filename is None:
            #filename = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'\\'+'pt.log'
            #filename = './pt.log'
            filename = rc.getConfigPath('filename')  + 'pt.log'
        self.filename = filename

        # 创建一个handler，用于写入日志文件 (每天生成1个，保留370天的日志)
        fh = logging.handlers.TimedRotatingFileHandler(self.filename, 'D', 1, 370,encoding='utf-8')
        fh.suffix = "%Y%m%d-%H%M.log"
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('[%(asctime)s] - %(filename)s [Line:%(lineno)d] - [%(levelname)s]-[thread:%(thread)s]-[process:%(process)s] - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.addHandler(fh)
        self.addHandler(ch)

if __name__ == '__main__':
    pass
