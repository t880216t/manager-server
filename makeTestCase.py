# -*-coding:utf-8-*-
import argparse,sys
import os,time
from threading import Thread

from app.static.interface_auto.common import common
from app.static.interface_auto.common import HttpUntil

# 测试脚本模板
test_case = """
# -*-coding:utf-8-*-
__author__ = "chenjian"
import os,sys,time,json
import unittest
sys.path.append("../../..")
from common import HttpUntil,common

class {save_file_name} (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_go(self):
        need_verif_value = 1
        need_save_responseData = 1
        url = {base_host} + {path}
        values = {parms}
        (responsedata,code) = HttpUntil.{method}(url,values,'')
        verif_parms = {verif_parms}
        if need_verif_value == {need_verif_value}:
            if code <300:
                new_verif_parms = verif_parms.split('], [')
                for item in new_verif_parms:
                    item = item.replace("'","")
                    item = item.split(', ')
                    verif_value = item[1]
                    if (item[2] == '1'):
                        _verif_value = common.get_value_from_key(verif_value)
                    else:
                        _verif_value = verif_value
                    
                    if common.verif_value_with_key(responsedata, item[0], _verif_value):
                        common.logInfo('Verif pass!')
                    else:
                        common.logInfo('Verif failed!')
                        common.logInfo(responsedata)
                        raise False
                if need_save_responseData == {need_save_responseData}:
                    common.saveToFile(responsedata, "{save_file_name}")
                    time.sleep(3)
                common.logInfo(responsedata)
            else:
                common.logInfo(responsedata)
                raise False
        else:
            if code < 300:
                if need_save_responseData == {need_save_responseData}:
                    common.saveToFile(responsedata,"{save_file_name}")
                    time.sleep(3)
                common.logInfo(responsedata)
            else:
                common.logInfo(responsedata)
                raise False

if __name__ == '__main__':

    unittest.main()

"""
old_run_case_data = """
# -*- coding: UTF-8 -*-
__author__ = 'jian.chen'

import unittest
import sys
sys.path.append("../..")
from common import HTMLTestRunner,HttpUntil,common
import time
import os
import subprocess

case_path = "src"
result = "result/"

def Creatsuite():
    #定义单元测试容器
    testunit = unittest.TestSuite()

    #定搜索用例文件的方法
    discover = unittest.defaultTestLoader.discover(case_path, pattern='Test_*.py', top_level_dir=None)

    #将测试用例加入测试容器中
    for test_suite in discover:
        for casename in test_suite:
            testunit.addTest(casename)
        print (testunit)
    return testunit

test_case = Creatsuite()

#获取系统当前时间
now = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
day = time.strftime('%Y-%m-%d', time.localtime(time.time()))

#定义个报告存放路径，支持相对路径
tdresult = result
if os.path.exists(tdresult):
    filename = tdresult + "/" + "result.html"
    fp = file(filename, 'wb')

    #定义测试报告
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'接口测试报告', description=u'用例详情：')

    #运行测试用例
    runner.run(test_case)
    fp.close()  #关闭报告文件
    url = 'http://127.0.0.1:5000/updateTaskStatus'
    values = {task_id}
    (responsedata,code) = HttpUntil.post(url, values, '')
    if responsedata['code'] == 0:
        common.logInfo('-------------run case over--------------')

else:
    os.mkdir(tdresult)
    filename = tdresult + "/" + "result.html"
    fp = file(filename, 'wb')

    #定义测试报告
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'接口测试报告', description=u'用例详情：')

    #运行测试用例
    runner.run(test_case)
    fp.close()  #关闭报告文件
    url = 'http://127.0.0.1:5000/updateTaskStatus'
    values = {task_id}
    (responsedata,code) = HttpUntil.post(url, values, '')
    if responsedata['code'] == 0:
        common.logInfo('-------------run case over--------------')
reuslt_file = open(filename)
result_data = reuslt_file.read()
common.Send_Mail(result_data, filename)
sys.exit(0)
"""

# 转换参数数据格式
def get_new_parms_data(parms_data):
    parms_data = parms_data
    new_parms_data = {}
    now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    for prams_item in parms_data:
        prams_item = prams_item.split(',')
        key = str(prams_item[1])
        value = str(prams_item[2].replace('#`#', ','))
        value_path = str(prams_item[4].replace('#`#', ','))
        isValueFromFile = str(prams_item[3])
        if isValueFromFile == "1":
            new_parms_data[key] = '|common.get_value_from_key("' + value_path + '")|'
        else:
            if value == 'now_email':
                new_parms_data[key] = now + '@test.test'
            elif value == 'now':
                new_parms_data[key] = now
            else:
                new_parms_data[key] = value
    new_parms_data = '{new_parms_data}'.format(new_parms_data=new_parms_data)
    new_parms_data = new_parms_data.replace("'|", '')
    new_parms_data = new_parms_data.replace("|'", '')
    return new_parms_data

# 转换校验参数数据格式
def get_new_verif_parms_data(parms_data):
    parms_data = parms_data
    new_parms_data = []
    for prams_item in parms_data:
        cache_data = []
        prams_item = prams_item.split(',')
        key = str(prams_item[1])
        value = str(prams_item[2].replace('#`#',','))
        isValueFromFile = str(prams_item[3])
        cache_data.append(key)
        cache_data.append(value)
        cache_data.append(isValueFromFile)
        new_parms_data.append(cache_data)
    new_parms_data = '{new_parms_data}'.format(new_parms_data=new_parms_data)
    new_parms_data = new_parms_data.replace("[[", '"')
    new_parms_data = new_parms_data.replace("]]", '"')
    return new_parms_data

# 生成测试脚本
def make_py_file(test_case, case_name, new_parms_data,new_verif_parms_data,verif_value, path, method, code, need_verif_value,
                 verif_value_from_file, verif_key, need_save_responseData,task_id,base_host):
    if verif_value_from_file == '1':
        _verif_value = 'common.get_value_from_key("' + verif_value + '")'
    else:
        _verif_value = '"'+verif_value+'"'
    test_case = test_case.format(
        path='"' + path + '"',
        parms=new_parms_data,
        verif_parms=new_verif_parms_data,
        method=method,
        code=code,
        need_verif_value=need_verif_value,
        verif_value_from_file=verif_value_from_file,
        verif_value=_verif_value,
        verif_key=verif_key,
        need_save_responseData=need_save_responseData,
        save_file_name=case_name,
        base_host='"' + base_host+ '"',
    )
    common.saveToFileAsPy(test_case, 'Test_' + case_name,task_id)

def loop_make_file(case_data,run_case_data,task_id,base_host):
    run_case_data = run_case_data.format(task_id='{"taskId":'+task_id+',"state": "3",}')
    common.saveRunPy(run_case_data, 'run_case',task_id)
    for case in case_data:
        # 用例名称
        case_name = case['test_name']
        # 请求路径
        path = case['path']
        # 请求类型：post_and_save_cookie,post,post_with_cookie,get,post_file
        method = case['method']
        # 模拟数据库返回参数
        try:
            parms_data = case['parms'].split("|~|")
            # 轮询数据参数并格式化处理
            new_parms_data = get_new_parms_data(parms_data)
        except:
            new_parms_data = '""'
        # 是否保存返回值：1保存
        need_save_responseData = case['need_save_response']
        # 验证服务端返回值code
        code = case['verif_code']
        # 是否验证返回值
        need_verif_value = case['need_verif_value']
        # 验证的key路径
        verif_key = case['verif_key']
        # 验证的值是否来自保存文件
        verif_value_from_file = case['verif_value_from_file']
        # 验证值
        verif_value = case['verif_value']
        # 模拟数据库返回参数
        try:
            verif_parms_data = case['verif_parms'].split("|~|")
            # 轮询数据参数并格式化处理
            new_verif_parms_data = get_new_verif_parms_data(verif_parms_data)
        except:
            new_verif_parms_data = '""'

        make_py_file(test_case, case_name, new_parms_data, new_verif_parms_data, verif_value, path, method, code, need_verif_value,
                     verif_value_from_file, verif_key, need_save_responseData,task_id,base_host)

newParser = argparse.ArgumentParser();
newParser.add_argument("-e", "--entry", dest="case_entry", help="Your need make case entry");
newParser.add_argument("-t", "--taskId", dest="task_id", help="Your need make case task id");
newParser.add_argument("-i", "--ip", dest="base_host", help="Your need make case domain");
args = newParser.parse_args();
if args.case_entry:
    args.case_entry = args.case_entry
else:
    args.case_entry = "0"
def run_case():
    os.system("python run_case.py")

entry = args.case_entry
task_id = args.task_id
base_host = args.base_host

# entry = '22'
# task_id = '14'
# base_host = 'http://app.xyz.cn'

#开始生成脚本
url = 'http://127.0.0.1:5000/interfaceList'
values = {
    #"entry": args.case_entry,
    "entry": entry,
}
(responsedata,code) = HttpUntil.post(url, values, '')
if responsedata['code'] == 0:
    case_date = responsedata['content']
    loop_make_file(case_date,old_run_case_data, task_id,base_host)
    Home = os.getcwd()
    common.logInfo('now you are in ' + Home)
    os.chdir(Home + '/app/static/interface_auto/test_src/' + task_id)
    os.system("python run_case.py")
    os.chdir(Home)
    common.logInfo('now you are in ' + os.getcwd())

sys.exit(0)
"""
调用方法：python makeTestCase.py -e 3,4 -t 123
"""
