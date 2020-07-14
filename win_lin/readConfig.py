#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/22 14:22
# @Author  : augus
# @FileName: readConfig.py
# @Software: PyCharm
import  configparser,os
configparser.RawConfigParser()
class readConfig(object):

    def __init__(self):
    # 属性（读取文件的参数）
        self.conf = configparser.RawConfigParser()
        config_path = os.path.dirname(__file__) + '\\' + 'config.ini'
        self.conf.read(config_path, encoding='utf-8-sig')
    #获取配置文件ConfigPath下的一个子项：
    def getConfigPath(self,name):
        readfile = self.conf.get('ConfigPath',name)
        return readfile

if __name__ == '__main__':

    re = readConfig()
    print('获取一个子项：',re.getConfigPath('filename'))
