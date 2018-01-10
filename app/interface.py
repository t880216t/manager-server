# -*- coding:utf-8 -*-
import MySQLdb
import os
from flask import make_response
from flask import render_template, flash, redirect, jsonify, Response
from app import app
from threading import Thread
from flask import request
from database_config import *

# 狗跨域
def cors_response(res):
    response = make_response(jsonify(res))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


@app.route('/addInterface', methods=['POST'])
def addInterface():
    # 获取上传参数 rowID,rowData,userID,
    test_name = request.values.get("test_name")
    path = request.values.get("path")
    method = request.values.get("method")
    parms = request.values.get("parms")
    verif_code = request.values.get("verif_code")
    need_save_response = request.values.get("need_save_response")
    need_verif_value = request.values.get("need_verif_value")
    verif_key = request.values.get("verif_key")
    verif_value_from_file = request.values.get("verif_value_from_file")
    verif_value = request.values.get("verif_value")
    test_description = request.values.get("test_description")
    project = request.values.get("project")
    datatype = request.values.get("datatype")
    verif_parms = request.values.get("verif_parms")

    # 入库
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')
    verif_sql = 'select * from interface_list WHERE test_name = %s'
    dbc.execute(verif_sql, (test_name,))
    verif_list = dbc.fetchall()
    if len(verif_list) > 0:
        dbc.close()
        db.close()
        response = cors_response({"code": 10001, "msg": "用例名称重复，"})
        return response

    sql = 'insert into interface_list (test_name, path, method, parms,verif_code,need_save_response,need_verif_value,verif_key,verif_value_from_file,verif_value,test_description,project,datatype,verif_parms) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    state = dbc.execute(sql, (
        test_name, path, method, parms, verif_code, need_save_response, need_verif_value, verif_key,
        verif_value_from_file,
        verif_value,test_description,project,datatype,verif_parms))

    if state:
        db.commit()
        response = cors_response({'code': 0, 'msg': '插入成功'})
        dbc.close()
        db.close()
        return response
    else:
        db.commit()
        response = cors_response({'code': 10001, 'msg': '插入失败'})
        dbc.close()
        db.close()
        return response

@app.route('/addprojectkey', methods=['POST'])
def addprojectkey():
    project_key = request.values.get("project_key")
    create_user = request.values.get("create_user")
    # 入库
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')
    verif_sql = 'select * from project_list WHERE project_key = %s'
    dbc.execute(verif_sql, (project_key,))
    verif_list = dbc.fetchall()
    if len(verif_list) > 0:
        dbc.close()
        db.close()
        response = cors_response({"code": 10001, "msg": "项目名称重复，"})
        return response

    sql = 'insert into project_list (project_key,create_user) VALUES (%s,%s)'
    state = dbc.execute(sql, (project_key,create_user))

    if state:
        db.commit()
        response = cors_response({'code': 0, 'msg': '插入成功'})
        dbc.close()
        db.close()
        return response
    else:
        db.commit()
        response = cors_response({'code': 10001, 'msg': '插入失败'})
        dbc.close()
        db.close()
        return response

@app.route('/updateInterface', methods=['POST'])
def updateInterface():
    # 获取上传参数 rowID,rowData,userID,
    entry = request.values.get("entry")
    test_name = request.values.get("test_name")
    path = request.values.get("path")
    method = request.values.get("method")
    parms = request.values.get("parms")
    verif_code = request.values.get("verif_code")
    need_save_response = request.values.get("need_save_response")
    need_verif_value = request.values.get("need_verif_value")
    verif_key = request.values.get("verif_key")
    verif_value_from_file = request.values.get("verif_value_from_file")
    verif_value = request.values.get("verif_value")
    test_description = request.values.get("test_description")
    project = request.values.get("project")
    datatype = request.values.get("datatype")
    verif_parms = request.values.get("verif_parms")
    # 入库
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')
    verif_sql = 'select * from interface_list WHERE test_name = %s'
    dbc.execute(verif_sql, (test_name,))
    verif_list = dbc.fetchone()
    if verif_list != None:
        if str(verif_list[0]) != str(entry):
            dbc.close()
            db.close()
            response = cors_response({"code": 10001, "msg": "用例名称重复，"})
            return response
    sql = 'update interface_list set test_name = %s, path = %s, method = %s, parms = %s,verif_code = %s,need_save_response = %s,need_verif_value = %s,verif_key = %s,verif_value_from_file = %s,verif_value = %s,test_description = %s ,project = %s ,datatype=%s ,verif_parms=%s where entry = %s'
    state = dbc.execute(sql, (test_name, path, method, parms, verif_code, need_save_response, need_verif_value, verif_key,verif_value_from_file,verif_value,test_description,project,datatype,verif_parms,entry))
    if state:
        db.commit()
        response = cors_response({'code': 0, 'msg': '修改成功'})
        dbc.close()
        db.close()
        return response
    else:
        db.commit()
        response = cors_response({'code': 0, 'msg': '未作任何修改'})
        dbc.close()
        db.close()
        return response

@app.route('/addInterfaceTask', methods=['POST'])
def addInterfaceTask():
    # 获取上传参数 rowID,rowData,userID,
    task_name = request.values.get("task_name")
    base_host = request.values.get("base_host")
    entry = request.values.get("entry")
    create_user = request.values.get("create_user")
    is_settime_task = request.values.get("is_settime_task")
    start_time = request.values.get("start_time")

    # 入库
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')

    sql = 'insert into interface_task_list (task_name, create_user, task_status, case_id,base_host,is_settime_task,start_time,settime_task_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
    state = dbc.execute(sql, (task_name,create_user, 0, entry,base_host,is_settime_task,start_time,1))
    if state:
        db.commit()
        response = cors_response({'code': 0, 'msg': '插入成功'})
        dbc.close()
        db.close()
        return response
    else:
        db.commit()
        response = cors_response({'code': 10001, 'msg': '插入失败'})
        dbc.close()
        db.close()
        return response

@app.route('/interfaceList', methods=['POST'])
def interfaceList():
    entry = request.values.get("entry")
    project = request.values.get("project")
    datatype = request.values.get("datatype")
    # 连接
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    # db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')
    if entry == '0':
        sql = 'select * from interface_list WHERE project = %s AND datatype =%s order by test_name asc'
        dbc.execute(sql,(project,datatype))
        list = dbc.fetchall()
    else:
        sql = 'select * from interface_list WHERE entry in (%s) order by test_name asc' % entry
        dbc.execute(sql)
        list = dbc.fetchall()
    if len(list) == 0:
        dbc.close()
        db.close()
        response = cors_response({"code": 10001, "msg": "还没有任务"})
        return response
    db.commit()
    result = []
    for obj in list:
        result.append({"entry": obj[0],
                       "test_name": obj[1],
                       "path": obj[2],
                       "method": obj[3],
                       "parms": obj[4],
                       "verif_code": obj[5],
                       "need_save_response": obj[6],
                       "need_verif_value": obj[7],
                       "verif_key": obj[8],
                       "verif_value_from_file": obj[9],
                       "verif_value": obj[10],
                       "test_description": obj[11],
                       "create_time": obj[12].strftime('%Y-%m-%d %H:%M:%S'),
                       "project": obj[13],
                       "datatype": obj[14],
                       "verif_parms": obj[15],
                       })
    response = cors_response({"code": 0, "content": result})
    dbc.close()
    db.close()
    return response

@app.route('/projectList', methods=['POST'])
def projectList():
    userName = request.values.get("userName")
    # 连接
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')
    sql = 'select * from project_list order by create_time asc'
    dbc.execute(sql)
    list = dbc.fetchall()
    if len(list) == 0:
        dbc.close()
        db.close()
        response = cors_response({"code": 10001, "msg": "还没有项目"})
        return response
    db.commit()
    result = []
    for obj in list:
        result.append({"entry": obj[0],
                       "project_key": obj[1],
                       "create_user": obj[2],
                       "create_time": obj[3],
                       })
    response = cors_response({"code": 0, "content": result})
    dbc.close()
    db.close()
    return response

@app.route('/interfaceTaskList', methods=['POST'])
def interfaceTaskList():
    # 连接
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')
    sql = 'select * from interface_task_list ORDER by create_time desc'
    dbc.execute(sql)
    list = dbc.fetchall()
    if len(list) == 0:
        dbc.close()
        db.close()
        response = cors_response({"code": 10001, "msg": "还没有任务"})
        return response
    db.commit()
    result = []
    for obj in list:
        result.append({"entry": obj[0],
                       "task_name": obj[1],
                       "create_user": obj[2],
                       "create_time": obj[3],
                       "task_status": obj[4],
                       "case_id": obj[5],
                       "is_settime_task": obj[7],
                       "start_time": obj[8],
                       "settime_task_status": obj[9],
                       })
    response = cors_response({"code": 0, "content": result})
    dbc.close()
    db.close()
    return response

@app.route('/interfaceTaskDetail', methods=['POST'])
def interfaceTaskDetail():
    entry = request.values.get("entry")
    # 连接
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')
    if entry == '0':
        sql = 'select * from interface_list'
        dbc.execute(sql)
        list = dbc.fetchall()
    else:
        task_sql = 'select case_id from interface_task_list where entry = %s'
        dbc.execute(task_sql, (entry,))
        case_id_list = dbc.fetchone()[0]
        sql = 'select * from interface_list WHERE entry in (%s)'%case_id_list
        dbc.execute(sql)
        list = dbc.fetchall()
    if len(list) == 0:
        dbc.close()
        db.close()
        response = cors_response({"code": 10001, "msg": "还没有任务"})
        return response
    db.commit()
    result = []
    for obj in list:
        result.append({"entry": obj[0],
                       "test_name": obj[1],
                       "path": obj[2],
                       "method": obj[3],
                       "parms": obj[4],
                       "verif_code": obj[5],
                       "need_save_response": obj[6],
                       "need_verif_value": obj[7],
                       "verif_key": obj[8],
                       "verif_value_from_file": obj[9],
                       "verif_value": obj[10],
                       "test_description": obj[11],
                       "create_time": obj[12].strftime('%Y-%m-%d %H:%M:%S'),
                       "project": obj[13],
                       "datatype": obj[14],
                       "verif_parms": obj[15],
                       })
    response = cors_response({"code": 0, "content": result})
    dbc.close()
    db.close()
    return response

def run_build(entry,taskId,baseHost):
    os.system("python makeTestCase.py -e " + taskId +" -t "+entry+" -i "+baseHost)

@app.route('/build', methods=['POST'])
def build():
    taskId = request.values.get("entry")
    # 连接
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')
    update_sql = 'update interface_task_list set task_status = "1" where entry = %s'
    state = dbc.execute(update_sql, (taskId,))
    db.commit()
    if state >= 0:
        sql = 'select * from interface_task_list WHERE entry = %s'
        dbc.execute(sql, (taskId,))
        obj = dbc.fetchone()
        entry = obj[5]
        baseHost = obj[6]
        t2 = Thread(target=run_build, args=(taskId, entry, baseHost))  # 指定目标函数，传入参数，这里参数也是元组
        t2.start()  # 启动线程
        dbc.close()
        db.close()
        response = cors_response({"code": 0, "msg": "正在生成脚本"})
        return response
    else:
        dbc.close()
        db.close()
        response = cors_response({'code': 10001, 'msg': '生成脚本失败'})
        return response


@app.route('/deleteInterface', methods=['GET', 'POST'])
def deleteInterface():
    # 获取上传参数 rowID,rowData,userID,
    if request.values.get("entry"):
        entry = request.values.get("entry")
        if entry.isdigit() == False:
            response = cors_response({'code': 10002, 'msg': '呵呵呵呵呵呵呵呵'})
            return response
    else:
        response = cors_response({'code': 10002, 'msg': '未获取到行数据'})
        return response

    # 入库
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')

    sql = 'delete from interface_list where entry = %s' % entry
    state = dbc.execute(sql)
    db.commit()

    if state:
        dbc.close()
        db.close()
        response = cors_response({'code': 0, 'msg': '删除成功'})
        return response
    else:
        dbc.close()
        db.close()
        response = cors_response({'code': 10001, 'msg': '删除失败'})
        return response

@app.route('/cloneInterface', methods=['GET', 'POST'])
def cloneInterface():
    # 获取上传参数 rowID,rowData,userID,
    if request.values.get("entry"):
        entry = request.values.get("entry")
        if entry.isdigit() == False:
            response = cors_response({'code': 10002, 'msg': '呵呵呵呵呵呵呵呵'})
            return response
    else:
        response = cors_response({'code': 10002, 'msg': '未获取到行数据'})
        return response
    test_name = request.values.get("clone_task_name")
    # 入库
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')

    verif_sql = 'select * from interface_list WHERE test_name = %s'
    dbc.execute(verif_sql, (test_name,))
    verif_list = dbc.fetchall()
    if len(verif_list) > 0:
        dbc.close()
        db.close()
        response = cors_response({"code": 10001, "msg": "用例名称重复"})
        return response

    need_value_sql = 'select * from interface_list WHERE entry = %s'%entry
    dbc.execute(need_value_sql)
    list = dbc.fetchone()
    path = list[2]
    method = list[3]
    parms = list[4]
    verif_code = list[5]
    need_save_response = list[6]
    need_verif_value = list[7]
    verif_key = list[8]
    verif_value_from_file = list[9]
    verif_value = list[10]
    test_description = list[11]
    project = list[13]
    datatype = list[14]
    verif_parms = list[15]

    sql = 'insert into interface_list (test_name, path, method, parms,verif_code,need_save_response,need_verif_value,verif_key,verif_value_from_file,verif_value,test_description,project,datatype,verif_parms) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    state = dbc.execute(sql, (
        test_name, path, method, parms, verif_code, need_save_response, need_verif_value, verif_key,
        verif_value_from_file,
        verif_value,test_description,project,datatype,verif_parms))

    if state:
        db.commit()
        dbc.close()
        db.close()
        response = cors_response({'code': 0, 'msg': '成功'})
        return response
    else:
        db.commit()
        dbc.close()
        db.close()
        response = cors_response({'code': 10001, 'msg': '失败'})
        return response

@app.route('/updateTaskStatus', methods=['GET', 'POST'])
def updateTaskStatus():
    # 获取上传参数 rowID,rowData,userID,
    if request.values.get("taskId"):
        taskId = request.values.get("taskId")
        state = request.values.get("state")
        if taskId.isdigit() == False:
            response = cors_response({'code': 10002, 'msg': '呵呵呵呵呵呵呵呵'})
            return response
    else:
        response = cors_response({'code': 10002, 'msg': '未获取到行数据'})
        return response

    # 入库
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')

    sql = 'update interface_task_list set task_status = %s where entry = %s'
    state = dbc.execute(sql,(state,taskId))
    db.commit()

    if state:
        dbc.close()
        db.close()
        response = cors_response({'code': 0, 'msg': '成功'})
        return response
    else:
        dbc.close()
        db.close()
        response = cors_response({'code': 10001, 'msg': '更新更新失败'})
        return response

@app.route('/closeSetTimeTask', methods=['GET', 'POST'])
def closeSetTimeTask():
    # 获取上传参数 rowID,rowData,userID,
    if request.values.get("taskId"):
        taskId = request.values.get("taskId")
        if taskId.isdigit() == False:
            response = cors_response({'code': 10002, 'msg': '呵呵呵呵呵呵呵呵'})
            return response
    else:
        response = cors_response({'code': 10002, 'msg': '未获取到行数据'})
        return response

    # 入库
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')

    sql = 'update interface_task_list set settime_task_status = %s where entry = %s'
    state = dbc.execute(sql,(0,taskId))
    db.commit()

    if state:
        dbc.close()
        db.close()
        response = cors_response({'code': 0, 'msg': '成功'})
        return response
    else:
        dbc.close()
        db.close()
        response = cors_response({'code': 10001, 'msg': '更新更新失败'})
        return response

@app.route('/getAutocompleteWords', methods=['GET', 'POST'])
def getAutocompleteWords():
    project = request.values.get("project")
    # 入库
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')
    if project == '':
        dbc.close()
        db.close()
        response = cors_response({"code": 10001, "msg": "请先选择项目"})
        return response

    sql = 'select test_name from interface_list where need_save_response = 1 and project = %s'
    dbc.execute(sql,(project,))
    list = dbc.fetchall()
    if len(list) == 0:
        dbc.close()
        db.close()
        response = cors_response({"code": 0, "msg": "还没有保存的返回值","content": [{"label": "暂无保存数据的用例"}]})
        return response
    db.commit()
    result = []
    for obj in list:
        if obj[0] == 'a_login':
            result.append({"label": "a_login.content.companyInfo.companyId"})
            result.append({"label": "a_login.content.userInfo.operatorId"})
        else:
            result.append({"label": obj[0]})
    response = cors_response({"code": 0, "content": result})
    dbc.close()
    db.close()
    return response
