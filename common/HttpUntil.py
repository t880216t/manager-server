# -*-coding:utf-8-*-
import requests

__author__ = "chenjian"

import time,json
import urllib
import urllib2
import cookielib
import common


"""
POST
"""
def post(url,parms,headers):
    try:
        data = urllib.urlencode(parms)
    except:
        data = parms
    if headers == '':
        req = urllib2.Request(url, data)
    else:
        req = urllib2.Request(url, data,headers)
    try:
        response = urllib2.urlopen(req)
        code = response.code
        responsedata = response.read()
        responsedata = json.loads(responsedata)
        return responsedata,code
    except Exception, e:
        print e
        return None,e.code


"""
POST and save cookie
"""
def post_and_save_cookie(url,parms,headers):
    fp = common.createFile('cookie')
    c = cookielib.LWPCookieJar(fp)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(c))
    try:
        data = urllib.urlencode(parms)
    except:
        data = parms
    if headers == '':
        req = urllib2.Request(url, data)
    else:
        req = urllib2.Request(url, data,headers)

    try:
        response = opener.open(req)
        code = response.code
        responsedata = response.read()
        responsedata = json.loads(responsedata)
        c.save(ignore_expires=True, ignore_discard=True)
        time.sleep(3)
        return responsedata,code

    except Exception, e:
        print e
        return None,e.code

"""
POST with cookie , make sure has the cookie first.
"""
def post_with_cookie(url,parms,headers):
    cookiefile = common.loadFilePath('cookie')
    assert cookiefile != None
    cookie = cookielib.LWPCookieJar()
    cookie.load(cookiefile, ignore_discard=True, ignore_expires=True)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    try:
        data = urllib.urlencode(parms)
    except:
        data = parms
    if headers == '':
        req = urllib2.Request(url, data)
    else:
        req = urllib2.Request(url, data,headers)


    try:
        response = opener.open(req)
        code = response.code
        responsedata = response.read()
        responsedata = json.loads(responsedata)
        return responsedata,code

    except Exception, e:
        print e
        return None,e.code

"""
GET
"""
def get(url,parms,headers):
    try:
        data = urllib.urlencode(parms)
    except:
        data = parms
    req = urllib2.Request(url,data)
    try:
        response = urllib2.urlopen(req)
        code = response.code
        responsedata = response.read()
        responsedata = json.loads(responsedata)
        return responsedata,code
    except Exception,e:
        print e
        return None,e.code


"""
post file
"""
def post_file(url,files):
    try:
        response = requests.post(url, files=files)
        code = response.code
        _response = response.content
        responsedata = json.loads(_response)
        return responsedata,code
    except Exception, e:
        print e
        return None,e.code
