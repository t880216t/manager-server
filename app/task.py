# -*- coding:utf-8 -*-
import MySQLdb
import os
import time

import sys
from flask import make_response
from flask import render_template, flash, redirect, jsonify, Response
from app import app
from threading import Thread
from flask import request
from bs4 import BeautifulSoup
from app.database_config import *

# 狗跨域
def cors_response(res):
    response = make_response(jsonify(res))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response

def LongToInt(value):
    assert isinstance(value, (int, long))
    return int(value & sys.maxint)

@app.route('/gettasklist', methods=['GET', 'POST'])
def get_task_list():
    if request.values.get("userID"):
        userID = request.values.get("userID")
    else:
        userID = 0

    # 连接
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')

    sql = 'select distinct project_id from case_list where user_id = %s'
    dbc.execute(sql,(userID,))
    project_ids = dbc.fetchall()
    if len(project_ids) == 0:
        dbc.close()
        db.close()
        response = cors_response({"code": 10001, "msg": "还没有任务"})
        return response
    relnewResult = []
    for project_id in project_ids:
        sql = 'select * from case_list where project_id = %s'
        #mysqldb版本兼容
        try:
            dbc.execute(sql, (project_id))
        except:
            dbc.execute(sql, (project_id,))
        sz = dbc.fetchall()
        totalCount = len(sz)
        doneCount = LongToInt(dbc.execute('select * from case_list where project_id = %s AND status = 1' % project_id))
        failedCount = LongToInt(dbc.execute('select * from case_list where project_id = %s AND status = 2' % project_id))
        def getchild(pid):
            result = []
            for obj in sz:
                if obj[2] == pid:
                    result.append({
                        "id": obj[0],
                        "title": obj[1].replace('$',''),
                        "pid": obj[2],
                        "entry": obj[7],
                        "status": obj[5],
                        "children": getchild(obj[0]),
                    })
            return result
        newResult = getchild(0)
        for item in range(1, len(newResult)):
            newResult[0]["children"].append(newResult[item])
        for item in range(1,len(newResult)):
            newResult.pop()
        newResult[0]['totalCount']=totalCount
        newResult[0]['doneCount']=doneCount
        newResult[0]['failedCount']=failedCount
        relnewResult.append(newResult[0])
    _result = {
        "code": 0,
        "content": relnewResult
    }
    response = cors_response(_result)
    dbc.close()
    db.close()
    return response

@app.route('/addcase', methods=['GET', 'POST'])
def addcase():
    entry = request.values.get("entry")
    title = request.values.get("newCase")
    # 连接
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')

    need_value_sql = 'select * from case_list WHERE entry = %s' % entry
    dbc.execute(need_value_sql)
    list = dbc.fetchone()
    pid = list[0]
    user_id = list[3]
    project_id = list[6]
    id_sql = "select max(id) from case_list where case_list.project_id = %s"
    dbc.execute(id_sql,(project_id,))
    ids = dbc.fetchone()
    id = ids[0]+1

    sql = 'insert into case_list (id,title,pid,user_id,status,project_id) VALUES (%s,%s,%s,%s,%s,%s)'
    state = dbc.execute(sql, (id,title,pid,user_id,0,project_id))
    if state:
        db.commit()
        dbc.close()
        db.close()
        response = cors_response({'code': 0, 'msg': '新建成功'})
        return response
    else:
        db.commit()
        dbc.close()
        db.close()
        response = cors_response({'code': 10001, 'msg': '新建失败'})
        return response

from werkzeug.utils import secure_filename
import os

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload():
    upload_file = request.files["file"]
    userID = request.values.get("userID")
    if upload_file:
        if allowed_file(upload_file.filename):
            # 连接
            db = MySQLdb.connect(database_host,database_username,database_password,database1)
            dbc = db.cursor()
            # 编码问题
            db.set_character_set('utf8')
            dbc.execute('SET NAMES utf8;')
            dbc.execute('SET CHARACTER SET utf8;')
            dbc.execute('SET character_set_connection=utf8;')

            projectID = int(round(time.time() * 1000))
            filename = secure_filename(upload_file.filename)
            #保存文件
            upload_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
            try:
                #读取文件信息
                file = open('app/static/uploads/'+filename).read()
                soup = BeautifulSoup(file)
                allData = []
                count = 1
                for k in soup.find_all('a'):
                    value = k.text.replace(u'\xa0', u'$')
                    allData.append([count, value])
                    count += 1
                sz = []
                allData[0].append(0)
                allData[1].append(0)
                sz.append(allData[0])
                sz.append(allData[1])
                #理出父子关系
                for i in range(len(allData)):
                    if i > 1:
                        prew_index = len(allData[i - 1][1]) - len(allData[i - 1][1].replace('$', ''))
                        now_index = len(allData[i][1]) - len(allData[i][1].replace('$', ''))
                        if now_index - prew_index == 1:
                            allData[i].append(allData[i - 1][0])
                        elif now_index - prew_index == 0:
                            try:
                                allData[i].append(allData[i - 1][2])
                            except:
                                print allData[i - 1]
                        elif now_index - prew_index < 0:
                            for l in range(0, len(sz)):
                                # 找新数组
                                _prew_index = len(sz[(len(sz) - 1) - l][1]) - len(sz[(len(sz) - 1) - l][1].replace('$', ''))
                                if now_index - _prew_index == 0:
                                    allData[i].append(sz[(len(sz) - 1) - l][2])
                                    break
                        sz.append(allData[i])
                for data in sz:
                    try:
                        sql = 'insert into case_list (id,title,pid,user_id,status,project_id) VALUES (%s,%s,%s,%s,%s,%s)'
                        dbc.execute(sql, (data[0],data[1].replace('$',''),data[2],userID,0,projectID))
                    except:
                        print (data[0])
                db.commit()
                dbc.close()
                db.close()
                response = cors_response({'code': 0, 'msg': '上传成功'})
                return response
            except:
                response = cors_response({'code': 10002, 'msg': '文件解析失败！只支持xmind导入出的纯html文件'})
                return response
        else:
            response = cors_response({'code': 10002, 'msg': '不支持的文件格式'})
            return response
    else:
        response = cors_response({'code': 10001, 'msg': '上传失败'})
        return response

@app.route('/settaskstatus', methods=['GET', 'POST'])
def settaskstatus():
    if request.values.get("entry"):
        entry = request.values.get("entry")
        status = request.values.get("status")
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
    sql = 'update case_list set status = %s where entry = %s'
    state = dbc.execute(sql,(status,entry))
    db.commit()
    need_value_sql = 'select * from case_list WHERE entry = %s' % entry
    dbc.execute(need_value_sql)
    list = dbc.fetchone()
    pid = list[2]
    project_id = list[6]
    if status == u'2':
        def updateFather(id):
            fasql = 'update case_list set status = 2 where id = %s and project_id = %s'
            dbc.execute(fasql,(id,project_id))
            db.commit()
            se_fasql = 'select * from case_list where id = %s and project_id = %s'
            dbc.execute(se_fasql, (id, project_id))
            se_list = dbc.fetchone()
            if id != 0:
                if se_list[2] != 0:
                    updateFather(se_list[2])
        updateFather(pid)
    if status == u'1':
        def updateFather(id):
            son_fail_sql = 'select * from case_list where pid = %s and project_id = %s  and status = 2'
            dbc.execute(son_fail_sql, (id,project_id))
            son_fail_list = dbc.fetchall()
            son_new_sql = 'select * from case_list where pid = %s and project_id = %s  and status = 0'
            dbc.execute(son_new_sql, (id, project_id))
            son_new_list = dbc.fetchall()
            if len(son_fail_list) == 0 and len(son_new_list) == 0:
                fasql = 'update case_list set status = 1 where id = %s and project_id = %s'
                dbc.execute(fasql,(id,project_id))
                db.commit()
                se_fasql = 'select * from case_list where id = %s and project_id = %s'
                dbc.execute(se_fasql, (id, project_id))
                se_list = dbc.fetchone()
                if id != 0:
                    if se_list[2] != 0:
                        updateFather(se_list[2])
            if len(son_fail_list) == 0 and len(son_new_list) > 0:
                fasql = 'update case_list set status = 0 where id = %s and project_id = %s'
                dbc.execute(fasql, (id, project_id))
                db.commit()
                se_fasql = 'select * from case_list where id = %s and project_id = %s'
                dbc.execute(se_fasql, (id, project_id))
                se_list = dbc.fetchone()
                if id != 0:
                    if se_list[2] != 0:
                        updateFather(se_list[2])
        updateFather(pid)
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

@app.route('/deletecase', methods=['GET', 'POST'])
def deletecase():
    entry = request.values.get("entry")
    # 入库
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')

    sql = 'select * from case_list WHERE entry = %s' % entry
    dbc.execute(sql)
    list = dbc.fetchone()
    id = list[0]
    project_id = list[6]
    if id == 1:
        project_sql = 'delete from case_list where project_id = %s'
        state = dbc.execute(project_sql,(project_id,))
        db.commit()
    else:
        son_sql = 'select * from case_list where pid = %s and project_id = %s '
        dbc.execute(son_sql, (id, project_id))
        son_list = dbc.fetchall()
        if len(son_list) > 0:
            dbc.close()
            db.close()
            response = cors_response({'code': 10002, 'msg': '请先其删除子用例'})
            return response
        else:
            delete_son_sql = 'delete from case_list WHERE entry = %s' % entry
            state = dbc.execute(delete_son_sql)
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
