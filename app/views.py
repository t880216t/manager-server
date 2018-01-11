# -*-coding:utf-8-*-
from app import app
import MySQLdb
from flask import request, jsonify
from flask import make_response
from database_config import *

@app.route('/')
@app.route('/index')
def index():
    return "Hello , Flask!"


"""
打开json文件
file_path = 'C:\Users\\xxxx\Desktop\qq\json\\nearby.json'
    with open(file_path) as json_file:
        data = json.load(json_file)
        user_data =  data["nearbyDataList"]
"""


@app.route('/add', methods=['GET', 'POST'])
def add():
    # 获取上传参数 rowID,rowData,userID,
    if request.values.get("rowID"):
        rowID = request.values.get("rowID")
    else:
        rowID = 0

    rowData = request.values.get("rowData")
    rowImage = request.values.get("imageUrl")

    if request.values.get("userID"):
        userID = request.values.get("userID")
    else:
        userID = 0

    if request.values.get("mianPid"):
        mianPid = request.values.get("mianPid")
    else:
        mianPid = 0

    # 入库
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')

    sql = 'insert into list (pid,labelname,userId,flag,mainpid,haschildren,testflag,isdone,imageUrl) VALUES (%s,%s,%s,0,%s,0,0,0,%s)'
    state = dbc.execute(sql, (rowID, rowData, userID, mianPid,rowImage))

    if state:
        updatePid_sql = "update list set haschildren = 1 where entry = %s" % rowID
        dbc.execute(updatePid_sql)
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


# 狗日的跨域
def cors_response(res):
    response = make_response(jsonify(res))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


# 转型数字
import sys


def LongToInt(value):
    assert isinstance(value, (int, long))
    return int(value & sys.maxint)


@app.route('/getlist', methods=['GET', 'POST'])
def get_list():
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
    sql = 'select * from list where userId = %s and isdone <> 1'
    dbc.execute(sql, (userID))
    list = dbc.fetchall()
    if len(list) == 0:
        dbc.close()
        db.close()
        response = cors_response({"code": 0, "msg": "还没有任务"})
        return response
    db.commit()

    def getChildren(pid):
        sz = []
        for obj in list:
            if obj[1] == pid:
                if pid == 0:
                    totalCount = dbc.execute('select * from list where mainpid = %s and haschildren = 0 ' % obj[0])
                    totalCount = LongToInt(totalCount)
                    if totalCount == 0:
                        totalCount = 1
                    _doneCount = dbc.execute(
                        'select * from list where mainpid = %s and haschildren = 0 and flag = 1' % obj[0])
                    _doneCount = LongToInt(_doneCount)
                    _testdoneCount = dbc.execute(
                        'select * from list where mainpid = %s and haschildren = 0 and flag = 0.5' % obj[0])
                    _testdoneCount = LongToInt(_testdoneCount)
                    _testdoneCount = float(_testdoneCount)/2
                    a = ((float(_doneCount)+_testdoneCount) / float(totalCount)) * 100
                    b = "%.1f" % a
                    Process = (b)
                if obj[1] != 0:
                    dbc.execute('select * from list where entry = %s' % obj[0])
                    isHasChildren = dbc.fetchall()
                    if isHasChildren[0][6] == 1:
                        totalCount = dbc.execute('select * from list where pid = %s' % obj[0])
                        totalCount = LongToInt(totalCount)
                        doneCount = dbc.execute('select * from list where pid = %s and flag = 1' % obj[0])
                        doneCount = LongToInt(doneCount)

                        testdoneCount = dbc.execute('select * from list where pid = %s and flag = 0.5' % obj[0])
                        testdoneCount = LongToInt(testdoneCount)
                        testdoneCount = float(testdoneCount) /2

                        if totalCount == 0:
                            totalCount = 1
                        Process = ((float(doneCount) + testdoneCount) / float(totalCount)) * 100
                        if Process == 100:
                            dbc.execute('update list set flag = 1 where entry = %s' % obj[0])
                            db.commit()
                        Process = "%.1f" % Process
                    else:
                        dbc.execute('select flag from list where entry = %s' % obj[0])
                        _childrenFlag = dbc.fetchone()
                        childrenFlag = _childrenFlag[0]
                        childrenProcess = childrenFlag
                        Process = childrenProcess * 100
                sz.append({"entry": obj[0],
                           "labelName": obj[2],
                           "process": Process,
                           "mainpid": obj[5],
                           "imageUrl": obj[9],
                           "children": getChildren(obj[0])})
        return sz

    newList = getChildren(0)
    response = cors_response(newList)
    dbc.close()
    db.close()
    return response

@app.route('/getdonelist', methods=['GET', 'POST'])
def get_done_list():
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
    sql = 'select * from list where userId = %s and isdone = 1'
    dbc.execute(sql, (userID))
    list = dbc.fetchall()
    if len(list) == 0:
        dbc.close()
        db.close()
        response = cors_response({"code": 0, "msg": "还没有任务"})
        return response
    db.commit()

    def getChildren(pid):
        sz = []
        for obj in list:
            if obj[1] == pid:
                if pid == 0:
                    totalCount = dbc.execute('select * from list where mainpid = %s and haschildren = 0 ' % obj[0])
                    totalCount = LongToInt(totalCount)
                    if totalCount == 0:
                        totalCount = 1
                    _doneCount = dbc.execute(
                        'select * from list where mainpid = %s and haschildren = 0 and flag = 1' % obj[0])
                    _doneCount = LongToInt(_doneCount)
                    _testdoneCount = dbc.execute(
                        'select * from list where mainpid = %s and haschildren = 0 and flag = 0.5' % obj[0])
                    _testdoneCount = LongToInt(_testdoneCount)
                    _testdoneCount = float(_testdoneCount)/2
                    a = ((float(_doneCount)+_testdoneCount) / float(totalCount)) * 100
                    b = "%.1f" % a
                    Process = (b)
                if obj[1] != 0:
                    dbc.execute('select * from list where entry = %s' % obj[0])
                    isHasChildren = dbc.fetchall()
                    if isHasChildren[0][6] == 1:
                        totalCount = dbc.execute('select * from list where pid = %s' % obj[0])
                        totalCount = LongToInt(totalCount)
                        doneCount = dbc.execute('select * from list where pid = %s and flag = 1' % obj[0])
                        doneCount = LongToInt(doneCount)

                        testdoneCount = dbc.execute('select * from list where pid = %s and flag = 0.5' % obj[0])
                        testdoneCount = LongToInt(testdoneCount)
                        testdoneCount = float(testdoneCount) /2

                        if totalCount == 0:
                            totalCount = 1
                        Process = ((float(doneCount) + testdoneCount) / float(totalCount)) * 100
                        if Process == 100:
                            dbc.execute('update list set flag = 1 where entry = %s' % obj[0])
                            db.commit()
                        Process = "%.1f" % Process
                    else:
                        dbc.execute('select flag from list where entry = %s' % obj[0])
                        _childrenFlag = dbc.fetchone()
                        childrenFlag = _childrenFlag[0]
                        childrenProcess = childrenFlag
                        Process = childrenProcess * 100
                sz.append({"entry": obj[0],
                           "labelName": obj[2],
                           "process": Process,
                           "mainpid": obj[5],
                           "imageUrl": obj[9],
                           "children": getChildren(obj[0])})
        return sz

    newList = getChildren(0)
    response = cors_response(newList)
    dbc.close()
    db.close()
    return response

@app.route('/getsharelist', methods=['GET', 'POST'])
def get_share_list():
    if request.values.get("mainID"):
        mainID = request.values.get("mainID")
    else:
        mainID = 0

    # 连接
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')
    sql = 'select * from list where entry = %s or mainpid = %s '
    dbc.execute(sql, (mainID,mainID))
    list = dbc.fetchall()
    if len(list) == 0:
        dbc.close()
        db.close()
        response = cors_response({"code": 0, "msg": "还没有任务"})
        return response
    db.commit()

    def getChildren(pid):
        sz = []
        for obj in list:
            if obj[1] == pid:
                if pid == 0:
                    totalCount = dbc.execute('select * from list where mainpid = %s and haschildren = 0' % obj[0])
                    totalCount = LongToInt(totalCount)
                    if totalCount == 0:
                        totalCount = 1
                    _doneCount = dbc.execute(
                        'select * from list where mainpid = %s and haschildren = 0 and flag = 1' % obj[0])
                    _doneCount = LongToInt(_doneCount)
                    _testdoneCount = dbc.execute(
                        'select * from list where mainpid = %s and haschildren = 0 and flag = 0.5' % obj[0])
                    _testdoneCount = LongToInt(_testdoneCount)
                    _testdoneCount = float(_testdoneCount)/2
                    a = ((float(_doneCount)+_testdoneCount) / float(totalCount)) * 100
                    b = "%.1f" % a
                    Process = (b)
                if obj[1] != 0:
                    dbc.execute('select * from list where entry = %s' % obj[0])
                    isHasChildren = dbc.fetchall()
                    if isHasChildren[0][6] == 1:
                        totalCount = dbc.execute('select * from list where pid = %s' % obj[0])
                        totalCount = LongToInt(totalCount)
                        doneCount = dbc.execute('select * from list where pid = %s and flag = 1' % obj[0])
                        doneCount = LongToInt(doneCount)

                        testdoneCount = dbc.execute('select * from list where pid = %s and flag = 0.5' % obj[0])
                        testdoneCount = LongToInt(testdoneCount)
                        testdoneCount = float(testdoneCount) /2

                        if totalCount == 0:
                            totalCount = 1
                        Process = ((float(doneCount) + testdoneCount) / float(totalCount)) * 100
                        if Process == 100:
                            dbc.execute('update list set flag = 1 where entry = %s' % obj[0])
                            db.commit()
                        Process = "%.1f" % Process
                    else:
                        dbc.execute('select flag from list where entry = %s' % obj[0])
                        _childrenFlag = dbc.fetchone()
                        childrenFlag = _childrenFlag[0]
                        childrenProcess = childrenFlag
                        Process = childrenProcess * 100
                sz.append({"entry": obj[0],
                           "labelName": obj[2],
                           "process": Process,
                           "mainpid": obj[5],
                           "imageUrl": obj[9],
                           "children": getChildren(obj[0])})
        return sz

    newList = getChildren(0)
    response = cors_response(newList)
    dbc.close()
    db.close()
    return response


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    # 获取上传参数 rowID,rowData,userID,
    if request.values.get("rowID"):
        rowID = request.values.get("rowID")
        if rowID.isdigit() == False:
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

    sql = 'delete from list where entry = %s' % rowID
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


@app.route('/done', methods=['GET', 'POST'])
def done():
    # 获取上传参数 rowID,rowData,userID,
    if request.values.get("rowID"):
        rowID = request.values.get("rowID")
        if rowID.isdigit() == False:
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

    #测试版情况
    dbc.execute('select testflag from list where entry = %s' % rowID)
    testflag = dbc.fetchone()[0]
    if testflag != 1:
        db.commit()
        dbc.close()
        db.close()
        response = cors_response({'code': 10002, 'msg': '请先完成测试版任务。'})
        return response

    sql = 'update list set flag = 1 where entry = %s' % rowID
    state = dbc.execute(sql)
    db.commit()

    if state:
        dbc.close()
        db.close()
        response = cors_response({'code': 0, 'msg': '完成任务成功'})
        return response
    else:
        dbc.close()
        db.close()
        response = cors_response({'code': 10001, 'msg': '任务设置失败'})
        return response

@app.route('/donetest', methods=['GET', 'POST'])
def donetest():
    # 获取上传参数 rowID,rowData,userID,
    if request.values.get("rowID"):
        rowID = request.values.get("rowID")
        if rowID.isdigit() == False:
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

    # 测试版情况
    dbc.execute('select testflag from list where entry = %s' % rowID)
    testflag = dbc.fetchone()[0]
    if testflag == 1:
        db.commit()
        dbc.close()
        db.close()
        response = cors_response({'code': 10002, 'msg': '测试版已完成。'})
        return response

    sql = 'update list set flag = 0.5 , testflag = 1 where entry = %s' % rowID
    state = dbc.execute(sql)
    db.commit()

    if state:
        dbc.close()
        db.close()
        response = cors_response({'code': 0, 'msg': '完成任务成功'})
        return response
    else:
        dbc.close()
        db.close()
        response = cors_response({'code': 10001, 'msg': '任务设置失败'})
        return response

@app.route('/donemain', methods=['GET', 'POST'])
def donemain():
    # 获取上传参数 rowID,rowData,userID,
    if request.values.get("rowID"):
        rowID = request.values.get("rowID")
        if rowID.isdigit() == False:
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

    sql = 'update list set isdone = 1 where entry = %s' % rowID
    state = dbc.execute(sql)
    db.commit()

    if state:
        dbc.close()
        db.close()
        response = cors_response({'code': 0, 'msg': '完成任务成功'})
        return response
    else:
        dbc.close()
        db.close()
        response = cors_response({'code': 10001, 'msg': '任务设置失败'})
        return response

@app.route('/donemainfalse', methods=['GET', 'POST'])
def donemainfalse():
    # 获取上传参数 rowID,rowData,userID,
    if request.values.get("rowID"):
        rowID = request.values.get("rowID")
        if rowID.isdigit() == False:
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

    sql = 'update list set isdone = 0 where entry = %s' % rowID
    state = dbc.execute(sql)
    db.commit()

    if state:
        dbc.close()
        db.close()
        response = cors_response({'code': 0, 'msg': '接着干成功'})
        return response
    else:
        dbc.close()
        db.close()
        response = cors_response({'code': 10001, 'msg': '任务设置失败'})
        return response


@app.route('/update', methods=['GET', 'POST'])
def update():
    # 获取上传参数 rowID,rowData,userID,
    if request.values.get("rowID"):
        rowID = request.values.get("rowID")
        if rowID.isdigit() == False:
            response = cors_response({'code': 10002, 'msg': '呵呵呵呵呵呵呵呵'})
            return response
    else:
        response = cors_response({'code': 10002, 'msg': '未获取到行数据'})
        return response

    rowData = request.values.get("rowData")
    rowImage = request.values.get("imageUrl")

    if request.values.get("userID"):
        userID = request.values.get("userID")
    else:
        userID = 0

    # 入库
    db = MySQLdb.connect(database_host,database_username,database_password,database1)
    dbc = db.cursor()
    # 编码问题
    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')

    sql = 'update list set labelname = %s , imageUrl = %s where entry = %s'
    state = dbc.execute(sql, (rowData, rowImage ,rowID))
    db.commit()

    if state:
        dbc.close()
        db.close()
        response = cors_response({'code': 0, 'msg': '编辑任务成功'})
        return response
    else:
        dbc.close()
        db.close()
        response = cors_response({'code': 10001, 'msg': '任务失败'})
        return response


# 简单的错误处理
class loginError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# 加密存储密码
import os
import hashlib


def encrypt_password(password, salt=None, encryptlop=30):
    if not salt:
        salt = os.urandom(16).encode('hex')  # length 32
    for i in range(encryptlop):
        password = hashlib.sha256(password + salt).hexdigest()  # length 64
    return password, salt


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        response = cors_response({'code': 10001, 'msg': '插入失败'})
        return response
    if request.method == 'POST':
        # 这里最好需要验证用户输入
        # 获取上传参数
        username = request.values.get("username")
        password = request.values.get("password")
        email = request.values.get("email")

        # 入库
        db = MySQLdb.connect(database_host,database_username,database_password,database1)
        dbc = db.cursor()
        # 编码问题
        db.set_character_set('utf8')
        dbc.execute('SET NAMES utf8;')
        dbc.execute('SET CHARACTER SET utf8;')
        dbc.execute('SET character_set_connection=utf8;')
        
        verif_sql = 'select * from users WHERE username = %s'
        dbc.execute(verif_sql, (username,))
        verif_list = dbc.fetchone()
        if verif_list != None:
            dbc.close()
            db.close()
            response = cors_response({"code": 10001, "msg": "用户登录名重复"})
            return response

        hash_password, salt = encrypt_password(password)
        dbc.execute('INSERT INTO users (username,hash_password,salt,email) VALUES (%s,%s,%s,%s)',
                    (username, hash_password, salt, email))
        db.commit()
        response = cors_response({'code': 0, 'msg': '注册成功'})
        dbc.close()
        db.close()
        return response


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        response = cors_response({'code': 10001, 'msg': '插入失败'})
        return response
    if request.method == 'POST':
        # 这里最好需要验证用户输入
        # 获取上传参数
        username = request.values.get("username")
        password = request.values.get("password")

        # 入库
        db = MySQLdb.connect(database_host,database_username,database_password,database1)
        dbc = db.cursor()
        # 编码问题
        db.set_character_set('utf8')
        dbc.execute('SET NAMES utf8;')
        dbc.execute('SET CHARACTER SET utf8;')
        dbc.execute('SET character_set_connection=utf8;')

        try:
            dbc.execute('SELECT `username` FROM users WHERE username = %s', (username,))
            if not dbc.fetchone():
                raise loginError(u'错误的用户名或者密码!')
            dbc.execute('SELECT `id`,`salt`,`hash_password` FROM users WHERE username = %s', (username,))
            id,salt, hash_password = dbc.fetchone()
            if encrypt_password(password, salt)[0] == hash_password:

                response = make_response(jsonify({'code': 0, 'msg': '登录成功','userID':id,'userName':username}))
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Methods'] = 'POST'
                response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
                response.set_cookie('userName', username)
                dbc.close()
                db.close()
                return response
            else:
                raise loginError('错误的用户名或者密码!')
        except loginError as e:
            dbc.close()
            db.close()
            response = cors_response({'code': 10001, 'msg': e.value})
            return response



@app.route('/signout', methods=['POST'])
def signout():
    response = make_response(jsonify({'code': 0, 'msg': '登出成功'}))
    response.set_cookie('username', '')
    return response
