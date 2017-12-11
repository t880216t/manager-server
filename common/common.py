# -*- coding:utf-8 -*-
__author__ = 'chenjian'

import time, os, sys,json,requests

def createFile(name):
    day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    # time.strftime('%Y-%m-%d', time.localtime(time.time()))
    result_data_dir = '/data'
    # tm = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
    type = ".txt"
    myname = name
    if os.path.exists('result'):
        fp = 'result' + result_data_dir
        if os.path.exists(fp) == False:
            os.mkdir(fp)
        filename = fp + "/" + myname + type
    else:
        fp = '../result' + result_data_dir
        if os.path.exists(fp) == False:
            os.makedirs(fp)
        filename = fp + "/" + myname + type

    return filename

def createFileAsPy(name,task_id):
    day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    # time.strftime('%Y-%m-%d', time.localtime(time.time()))
    result_data_dir = '/'+task_id + '/src'
    tm = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    type = ".py"
    myname = name
    if os.path.exists('app/static/interface_auto/test_src'):
        fp = 'app/static/interface_auto/test_src' + result_data_dir
        if os.path.exists(fp) == False:
            os.mkdir(fp)
        filename = fp + "/" + myname + type

    else:
        fp = '../app/static/interface_auto/test_src' + result_data_dir
        if os.path.exists(fp) == False:
            os.mkdir(fp)
        filename = fp + "/" + myname + type

    return filename

def createRunPy(name,task_id):
    day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    # time.strftime('%Y-%m-%d', time.localtime(time.time()))
    result_data_dir = '/'+task_id
    # tm = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
    type = ".py"
    myname = name
    if os.path.exists('app/static/interface_auto/test_src'):
        fp = 'app/static/interface_auto/test_src' + result_data_dir
        if os.path.exists(fp) == False:
            os.mkdir(fp)
        filename = fp + "/" + myname + type
    else:
        fp = '../app/static/interface_auto/test_src' + result_data_dir
        if os.path.exists(fp) == False:
            os.mkdir(fp)
        filename = fp + "/" + myname + type
    return filename

def saveToFileAsPy(data,fileName,task_id):
    fp = createFileAsPy(fileName,task_id)
    savefile = open(fp, 'w')
    savefile.writelines(data)
    savefile.close()
    time.sleep(3)
    logInfo('save data to file :' + fp)

def saveRunPy(data,fileName,task_id):
    fp = createRunPy(fileName,task_id)
    savefile = open(fp, 'w')
    savefile.writelines(data)
    savefile.close()
    time.sleep(3)
    logInfo('save data to file :' + fp)

def saveToFile(data,fileName):
    fp = createFile(fileName)
    savefile = open(fp, 'w')
    data = json.dumps(data)
    savefile.write(data)
    savefile.close()
    time.sleep(3)
    logInfo('save data to file :' + fp)

def loadFilePath(fileName):
    # 获取本地cookie
    day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    fp = "../result" + "/data"
    type = ".txt"
    myname = fileName
    cookiefile = fp + "/" + myname + type
    if os.path.exists(cookiefile):
        return cookiefile
    else:
        fp = "result"+ "/data"
        type = ".txt"
        myname = fileName
        cookiefile = fp + "/" + myname + type
        if os.path.exists(cookiefile):
            return cookiefile
        else:
            print ("Error: has not file ,please check it on "+cookiefile)
            return None

def loadFileData(fileName):
    fp = loadFilePath(fileName)
    data = open(fp).read()
    data = json.loads(data)
    return data


# 获取用户指定响应字段值，与设定值对比
def verif_value_with_key(responseData, verif_key, verif_value):
    a = verif_key.split(".")
    data = responseData
    c = len(a)
    need_data = data
    for i in range(0, c):
        key =  a[i]
        if key == '0':
            key = 0
        need_data = need_data[key]
    if need_data == verif_value:
        return True
    else:
        logInfo(need_data+'|'+verif_value)
        return False

#获取用户输入的val路径拉取保存文件中的值
def get_value_from_key(key):
    input_data = key
    a = input_data.split(".")
    b = a[0]
    data = loadFileData(b)
    c = len(a)
    need_data = data
    for i in range(1,c):
        key = a[i]
        if key == '0':
            key = 0
        need_data = need_data[key]
    return need_data

#带时间log打印
def logInfo(str):
    #lineNumber = sys._getframe().f_back.f_lineno  # 获取行号
    logtime =  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print logtime,str
