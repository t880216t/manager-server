# -*- coding:utf-8 -*-
import MySQLdb
from flask import make_response
from flask import render_template, flash, redirect,jsonify,Response
from app import app
import json
from flask import request
from database_config import *

#狗日的跨域
def cors_response(res):
    response = make_response(jsonify(res))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response

@app.route('/addProd', methods=['GET', 'POST'])
def addProd():
    # 获取上传参数
    print 'here------------------'
    titleContent = request.values.get("titleContent")
    titleImage = request.values.get("titleImage")
    price = request.values.get("price")
    condition = request.values.get("condition")
    description = request.values.get("desc")
    imageUrls = request.values.get("imageUrls")
    userId = request.values.get("userId")
    
    print (titleContent,price,condition,description,titleImage,imageUrls,userId)

    # 入库
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')

    sql = 'insert into prod (title,price,chense,description,title_image,image_urls,user_id) VALUES (%s,%s,%s,%s,%s,%s,%s)'
    state = dbc.execute(sql,(titleContent,price,condition,description,titleImage,imageUrls,userId))

    if state:
        db.commit()
        response = cors_response({'code': 0, 'msg': '插入成功'})
        return response
    else:
        db.commit()
        response = cors_response({'code': 10001, 'msg': '插入失败'})
        return response

from flask import Flask, request
from werkzeug.utils import secure_filename
import os

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/uploadfile', methods=['POST'])
def uploadfile():
    upload_file = request.files["file"]
    if upload_file and allowed_file(upload_file.filename):
        filename = secure_filename(upload_file.filename)
        upload_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
        imageUrl = 'http://ownerworld.win:5000/' + 'static/uploads/' + filename
        response = cors_response({'code': 0, 'msg': '上传成功','url':imageUrl})
        return response
    else:
        response = cors_response({'code': 10001, 'msg': '上传失败'})
        return response



@app.route('/getmyprodlist', methods=['POST'])
def get_my_prod_list():

    userID = request.values.get("userID")
    # 连接
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')
    sql = 'select * from prod where user_id = %s order by create_time desc'
    dbc.execute(sql, (userID,))
    list = dbc.fetchall()
    if len(list) == 0:
        dbc.close()
        db.close()
        response = cors_response({"code": 0, "msg": "未找到提交记录"})
        return response
    prods = []
    for obj in list:
        prods.append({"id": obj[0],
                   "title": obj[1],
                   "price": obj[2],
                   "chense": obj[3],
                   "titleImage": obj[5],
                   "createTime": obj[8],
                   "state": obj[9]})

    response = cors_response(prods)
    dbc.close()
    db.close()
    return response
	
@app.route('/getprodlist', methods=['POST'])
def get_prod_list():
    prodName = request.values.get("prodName")
    # 连接
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')
    if prodName == u'':
        sql = 'select * from prod where state = 1 order by create_time desc'
        dbc.execute(sql)
    else:
        sql = "select * from prod where state = 1 and title like '%"+prodName+"%' order by create_time desc"
        dbc.execute(sql)


    list = dbc.fetchall()
    if len(list) == 0:
        dbc.close()
        db.close()
        response = cors_response({"code": 0, "msg": "未找到提交记录"})
        return response
    prods = []
    for obj in list:
        prods.append({"id": obj[0],
                      "title": obj[1],
                      "price": obj[2],
                      "chense": obj[3],
                      "titleImage": obj[5],
                      "createTime": obj[8],
                      "state": obj[9]})

    response = cors_response(prods)
    dbc.close()
    db.close()
    return response
	
@app.route('/getproddetail', methods=['POST'])
def get_prod_detail():
    prodId = request.values.get("prodId")
    # 连接
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')
    sql = 'select * from prod where id = %s order by create_time desc'
    dbc.execute(sql, (prodId,))
    list = dbc.fetchall()
    if len(list) == 0:
        dbc.close()
        db.close()
        response = cors_response({"code": 0, "msg": "未找到提交记录"})
        return response
    prods = []
    for obj in list:
        prods.append({"id": obj[0],
                      "title": obj[1],
                      "price": obj[2],
                      "chense": obj[3],
                      "description": obj[4],
                      "titleImage": obj[5],
                      "imageUrls": obj[6],
                      "createTime": obj[8],
                      "state": obj[9]})

    response = cors_response(prods)
    dbc.close()
    db.close()
    return response



