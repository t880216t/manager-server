# -*- coding:utf-8 -*-
import MySQLdb
import os
import time
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
        dbc.execute(sql, (project_id,))
        sz = dbc.fetchall()
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
        relnewResult.append(newResult[0])
    _result = {
        "code": 0,
        "content": relnewResult
    }
    response = cors_response(_result)
    dbc.close()
    db.close()
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
    if upload_file and allowed_file(upload_file.filename):
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
        #读取文件信息
        file = open('app/static/uploads/test.html').read()
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
    else:
        response = cors_response({'code': 10001, 'msg': '上传失败'})
        return response

