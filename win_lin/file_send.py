#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/12 0012 14:39
# @Author  : augus
# @FileName: file_send.py
# @Software: PyCharm
# !/usr/bin/env python
# coding: utf-8
import paramiko
import datetime
import os
import sqlite3
from readConfig import readConfig#导入读取配置文件模块
from loggerConfig import Logger#导入日志模块
log = Logger()
rc = readConfig()
hostname = rc.getConfigPath('hostname')
username = rc.getConfigPath('username')
password = str(rc.getConfigPath('password'))
port = int(rc.getConfigPath('port'))

def upload(local_dir, remote_dir):
    try:
        t = paramiko.Transport((hostname, port))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        log.info('上传开始：%s ' % datetime.datetime.now())
        for root, dirs, files in os.walk(local_dir):
            log.info('文件存储路径及上传文件：[%s][%s]' % (root, files))
            if files.__len__()==0:
                log.info(f'{root}路径下为空，无文件')
                startTime1 = datetime.datetime.now()
                endTime = datetime.datetime.now()
                insertIntoInfo(startTime1, endTime, "", 0, f'{root}路径下为空，无文件')
                break;
            else:
                for filespath in files:
                    startTime = datetime.datetime.now()  # 开始时间
                    local_file = os.path.join(root, filespath)
                    log.info('目标文件及路径：[%s][%s]' % ( filespath, local_file))
                    a = local_file.replace(local_dir, '').replace('\\', '/').lstrip('/')
                    log.info(f'传输文件：{a}，存储目录：{remote_dir}')
                    remote_file = os.path.join(remote_dir, a)
                    log.info('远程路径及文件名称：%s'%remote_file)
                    try:
                        sftp.put(local_file, remote_file)
                        salary = 1
                        sign = ""
                        endTime = datetime.datetime.now()
                        insertIntoInfo(startTime, endTime, a, salary, sign)
                    except Exception as result:
                        sftp.mkdir(os.path.split(remote_file)[0])
                        log.info("创建文件夹成功")
                        sftp.put(local_file, remote_file)
                        log.info("上传本地文件 %s 到linux服务器%s：" % (local_file, remote_file))
            log.info('文件传输成功:%s ' % datetime.datetime.now())
        t.close()
    except Exception as result:
        salary = 0
        sign = result
        log.error('报错信息:%s'%result)
        endTime = datetime.datetime.now()
        insertIntoInfo(startTime, endTime, a, salary, sign)
    finally:
        log.info('文件传输结束')
def insertIntoInfo(startTime,endTime,fileName,salary,sign):
    db_path = rc.getConfigPath('db_path')
    conn = sqlite3.connect(db_path)  # 建立连接
    log.info("Open database successfully")
    cursor = conn.cursor()  # 创建cursor
    cursor.execute("INSERT INTO logs_db (FILE_NAME,ST_TIME,END_TIME,SALARY,SIGN) VALUES ('%s', '%s', '%s', %s, '%s' );"%(fileName,startTime,endTime,salary,sign))
    cursor.close()# 关闭cursor
    conn.commit()# 提交事务
    conn.close() # 关闭连接

if __name__ == '__main__':
    local_dir = rc.getConfigPath('local_dir')
    remote_dir = rc.getConfigPath('remote_dir')
    upload(local_dir, remote_dir)