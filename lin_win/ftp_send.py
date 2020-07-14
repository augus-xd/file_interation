#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/7/14 0014 15:01
# @Author  : augus
# @FileName: ftp_send.py
# @Software: PyCharm

import datetime
import os
import sqlite3
from readConfig import readConfig#导入读取配置文件模块
from loggerConfig import Logger#导入日志模块
from ftplib import FTP
#实例化类
log = Logger()
rc = readConfig()

#定义上传方法
def ftpTransport(local_dir, remote_dir,ip_address,ip_port,username,password):
    startTime = datetime.datetime.now()
    endTime = datetime.datetime.now()
    try:
        #连接ftp
        log.info('上传开始：%s ' % datetime.datetime.now())
        f = FTP()
        f.connect(ip_address, ip_port)
        f.login(username, password)
        f.encoding = 'gbk'
        f.cwd(remote_dir)
        #循环目录下的所有文件
        for root, dirs, files in os.walk(local_dir):
            log.info('文件存储路径及上传文件：[%s][%s]' % (root, files))
            if files.__len__()==0:
                log.info(f'{root}路径下为空，无文件')
                insertIntoInfo(startTime, endTime, "", 0, f'{root}路径下为空，无文件')#调用写日志到数据库方法
                break;
            else:
                for filespath in files:
                    local_file = os.path.join(root, filespath)
                    log.info('目标文件及路径：[%s][%s]' % ( filespath, local_file))
                    a = local_file.replace(local_dir, '').replace('\\', '/').lstrip('/')
                    log.info(f'传输文件：{a}，存储目录：{remote_dir}')
                    remote_file = os.path.join(remote_dir, a)
                    log.info('远程路径及文件名称：%s'%remote_file)
                    try:
                        #进行文件传输
                        filename = os.path.basename(a)
                        fd = open(local_file, 'rb')
                        # f.storbinary('STOR %s' % os.path.basename(localfile,),fd)
                        log.info("打开文件夹成功")
                        f.storbinary('STOR %s' % (filename), fd)
                        log.info("上传本地文件 %s 到linux服务器%s：" % (local_file, remote_file))
                        salary = 1
                        sign = ""
                        insertIntoInfo(startTime, endTime, a, salary, sign)
                    except Exception as result:
                        log.info(f'错误信息为:{result}')
                    finally:
                        #print('文件读取完毕')
                        fd.close()
            log.info('文件传输成功:%s ' % datetime.datetime.now())
    except Exception as result:
        salary = 0
        sign = result
        insertIntoInfo(startTime, endTime, a, salary, sign)
        log.error('报错信息:%s' % result)
    finally:
        log.info('文件传输结束')
        f.quit()
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
    ip_address = rc.getConfigPath('hostname')
    ip_port = int(rc.getConfigPath('port'))
    username = rc.getConfigPath('username')
    password = rc.getConfigPath('password')
    ftpTransport(local_dir, remote_dir,ip_address,ip_port,username,password)