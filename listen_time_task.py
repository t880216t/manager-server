#-*-coding:utf-8-*-
import os,sys,time,MySQLdb
import datetime,os
import time
import shutil
from app.static.interface_auto.common import HttpUntil
from app.static.interface_auto.common import common
from app.database_config import *

#删除原有文件夹
def init_task_dir(taskId):
    task_dir = 'app/static/interface_auto/test_src/' + str(taskId)
    if os.path.exists(task_dir):
        print 'test'
        delList = []
        delDir = task_dir
        delList = os.listdir(delDir)
        if len(delList) > 0:
            for f in delList:
                filePath = os.path.join(delDir, f)
                if os.path.isfile(filePath):
                    os.remove(filePath)
                    common.logInfo( filePath + " was removed!")
                elif os.path.isdir(filePath):
                    shutil.rmtree(filePath, True)
                common.logInfo("Directory: " + filePath + " was removed!")
        os.rmdir(task_dir)
        common.logInfo("Directory: " + task_dir + " was removed!")
    else:
        common.logInfo( 'have no dir:'+ task_dir)

def doSth(taskId):
    init_task_dir(taskId)
    # 开始生成脚本
    url = 'http://127.0.0.1:5000/build'
    values = {
        "entry": taskId,
    }
    (responsedata,code) = HttpUntil.post(url, values, '')
    if responsedata:
        if responsedata['code'] == 0:
            common.logInfo( 'run and build settime task:'+str(taskId))
    else:
        common.logInfo('can not connect to the server , please check if it has been runned')
    time.sleep(60)

def main():
    print 'listen run start'
    while True:
        while True:
            # 入库
            try:
                db = MySQLdb.connect(database_host,database_username,database_password,database1)
                dbc = db.cursor()
                # 编码问题
                db.set_character_set('utf8')
                dbc.execute('SET NAMES utf8;')
                dbc.execute('SET CHARACTER SET utf8;')
                dbc.execute('SET character_set_connection=utf8;')
                sql = 'select * from interface_task_list where is_settime_task = 1 and settime_task_status = 1'
                dbc.execute(sql)
                list = dbc.fetchall()
                dbc.close()
                db.close()
            except:
                common.logInfo("lost mysql connect!")
                time.sleep(60)
                continue
            task_data= []
            for obj in list:
                taskId = obj[0]
                start_time = obj[8]
                task_data.append([taskId,start_time])
            logtime = time.strftime('%H:%M', time.localtime(time.time()))
            print task_data,logtime
            for item in task_data:
                if item[1] == str(logtime):
                    doSth(item[0])
                    break
            time.sleep(60)


start_listen = main()
