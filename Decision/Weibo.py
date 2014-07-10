# -*- coding: utf-8 -*-



import urllib2
import urllib
import cookielib
import logging
import re
import sys
import os
import codecs
import json
import base64
import rsa
import binascii
import time
import random

from bs4 import BeautifulSoup
from datetime import datetime

'''
subpage:
example:http://blog.sina.com.cn/s/article_sort_1594987341_10001_2.html

simulate user login and start getting data

test url http://www.weibo.com/shaiwuguangchang

Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Encoding:gzip,deflate,sdch
Accept-Language:en-US,en;q=0.8,it;q=0.6,ja;q=0.4,zh-CN;q=0.2,zh-TW;q=0.2
Cookie:login_sid_t=ae37fcd613865e993cad00d346716634; YF-Ugrow-G0=062d74e096398759b246e61a81b65c98; _s_tentry=-; Apache=8825682110618.8.1404802769233; SINAGLOBAL=8825682110618.8.1404802769233; ULV=1404802769254:1:1:1:8825682110618.8.1404802769233:; SUS=SID-1581299170-1404802783-GZ-m63t8-ab075d3bf96e8237073752473308f170; SUE=es%3D112e63d6f407df7004fc12f0aca5ada3%26ev%3Dv1%26es2%3D57c6a020daa6de1349a9b191d8b44777%26rs0%3DJQFyZqumi%252BIuuCC0Lr5UBK0lCa%252FwDqw5p%252BY243dHfgITU8FhJIAiQcTgdkWfIKU8mZ4EMtoGB4YkUQqRTFJg8MjWsgZCmW9vtQKjtb9iddG6AOKC0dpEyfmsXZTP1js3ScgKWcEfxcZF1bma4%252BSJuDHqzTPlwAHcqXGVk333R58%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1404802783%26et%3D1404889183%26d%3Dc909%26i%3Df170%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D0%26st%3D0%26uid%3D1581299170%26name%3Djasonnk%2540163.com%26nick%3DJason%25E5%259C%25A8%25E6%25B0%25B4%25E4%25B8%2580%25E6%2596%25B9%26fmp%3D%26lcp%3D2012-02-09%252022%253A29%253A53; SUB=AR0%2BhbWmi%2FjCzymsz0jGyOzTZ4qP4ZaCbdOuzhhl1f1SMoBKjq1ngcyelTMifsDDbn1EvgYHfcXhnq4sGOzhwpQmFxcPB9lZ%2F2K0iQi2ZbULipr6pbVFAPFGpEiOlozwDm%2Bn7b8Bqz9v%2FIjvjflyhOc%3D; SUBP=002A2c-gVlwEm1uAWxfgXELuuu1xVxBxAL6eT5a69KOv6NqqdxLyq8TuHY-u_1%3D; ALF=1436338783; SSOLoginState=1404802783; un=jasonnk@163.com
Host:www.weibo.com
Proxy-Connection:keep-alive
Referer:http://www.weibo.com/login.php
User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2015.0 Safari/537.36

'''

if os.path.exists('app.log'):
    os.remove('app.log')

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(message)s')


FORWARD = [u'大赞，太好了！很支持', u'真不错',u'深有感触！',u'太好，真是极品',u'为什么刚看到',u'支持！支持！支持！']

class Weibo(object):
    """docstring for Weibo"""
    def __init__(self):
        super(Weibo, self).__init__()
        #init
        #init urllib2
        #proxyHandler = urllib2.ProxyHandler({'http':'http://10.40.14.56:8080'})

        cookie = cookielib.CookieJar()
        cookieHandler = urllib2.HTTPCookieProcessor(cookie)
        #opener = urllib2.build_opener(proxyHandler, cookieHandler)
        opener = urllib2.build_opener(cookieHandler)
        urllib2.install_opener(opener)


    def Login(self):
        data = {'1':'2'}
        self.req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2015.0 Safari/537.36',
                      'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                      #'Accept-Encoding':'gzip,deflate,sdch',
                      'Accept-Language':'en-US,en;q=0.8,it;q=0.6,ja;q=0.4,zh-CN;q=0.2,zh-TW;q=0.2',
                      #'Referer':'http://passport.weibo.com/visitor/visitor?a=enter&url=http%3A%2F%2Fweibo.com%2Fshaiwuguangchang&_rand=1404802028.4942'
                      }

        #http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.18)&_=1404822913046
        preloginURL = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.18)'
        request = urllib2.Request(preloginURL, None, self.req_header)
        resp = urllib2.urlopen(request)
        st = resp.read()
        m = re.search('\((.*)\)', st)
        if m:
            decodedJson = json.loads(m.group(1))
        logging.debug(decodedJson)

        loginURL = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
        username = 'jasonnk@163.com'
        password = 'sparkman'

        username = base64.b64encode(urllib.quote(username))

        pubkey = decodedJson['pubkey']
        servertime = decodedJson['servertime']
        nonce = decodedJson['nonce']
        rsakv = decodedJson['rsakv']

        password = self.get_pwd(password, servertime, nonce, pubkey)

        data = {'entry':'weibo',
                'gateway' : '1',
                'from' : '',
                'savestate' : '7',
                'useticket' : '1',
                'vsnf' : '1',
                'service' : 'miniblog',
                'pwencode' : 'rsa2',
                'servertime' : servertime,
                'nonce' : nonce,
                'rsakv' : rsakv,
                'su' : username,
                'sp' : password,
                'sr' : '1600*900',
                'encoding' : 'UTF-8',
                'prelt' : '115',
                'url' : 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
                'returntype' : 'META'
        }
        logging.debug(data)

        request = urllib2.Request(loginURL, urllib.urlencode(data), self.req_header)
        resp = urllib2.urlopen(request)
        m = re.search(r'location.replace\(\'(.*?)\'\)', resp.read())
        if m:
            logging.debug(m.group(1))
            url = m.group(1)
            #do login
            request = urllib2.Request(url, None, self.req_header)
            resp = urllib2.urlopen(request)
            #login ok
            print 'Login OK'
        else:
            print 'Login Failed'
        

    def PrepareRequest(self, url):
        self.baseURL = url

        request = urllib2.Request(url, None, self.req_header)
        resp = urllib2.urlopen(request)
        #do nothing
        #$CONFIG['page_id']='1002062093492691'; 
        #$CONFIG['domain']='100206'; 
        logging.debug('---------------------------------------------------------------')
        for line in resp.read().split('\r\n'):
            m = re.search('CONFIG\[\'page_id\'\]=\'(\d+)\';', line)
            if m:
                self.id = m.group(1)
            m = re.search('CONFIG\[\'domain\'\]=\'(\d+)\';', line)
            if m:
                self.domain = m.group(1)
            m = re.search('CONFIG\[\'uid\'\]=\'(\d+)\';', line)
            if m:
                self.uid = m.group(1)
            m = re.search('"pl.content.homeFeed.index","domid":"(.*?)"', line)
            if m:
                self.pids = m.group(1)

        logging.debug('---%s---%s---%s---' % (self.id, self.domain, self.pids))


    def Request(self, url):
        logging.debug('####->Request Page[%s]' % (url))

        request = urllib2.Request(url, None, self.req_header)
        resp = urllib2.urlopen(request)

        content = resp.read()
        #logging.debug(content)

        i = content.find('<script>parent.FM.view(')
        i = i + len('<script>parent.FM.view(')
        j = content.rfind(')</script>')
        #logging.debug(content[i:j])
        
        decodeStr = json.loads(content[i:j])
        html = decodeStr['html']
        #logging.debug(html)

        self.Analyze(html)

        self.pagebar = 0

        return True

    def GetPageURL(self, page):
        url = '%s?pids=%s&is_search=0&visible=0&is_tag=0&profile_ftype=1&page=%d&ajaxpagelet=1' % (self.baseURL, self.pids, page)
        return url

    def RequestWithScroll(self, page):
        logging.debug('##################->Request Page[%d] with Scroll' % (page))

        #http://weibo.com/p/aj/mblog/mbloglist?_wv=5&domain=100206&pre_page=3&page=3&max_id=3727809274986773&end_id=3727951835174987&count=15&pagebar=0&max_msign=&filtered_min_id=&pl_name=Pl_Official_LeftProfileFeed__55&id=1002062093492691&script_uri=/u/2093492691&feed_type=0&is_search=0&visible=0&is_tag=0&profile_ftype=1&__rnd=1404862769035
        #http://weibo.com/p/aj/mblog/mbloglist?_wv=5&domain=100206&pre_page=3&page=3&count=15&pagebar=0&id=1002062093492691&script_uri=/u/2093492691&feed_type=0&is_search=0&visible=0&is_tag=0&profile_ftype=1&__rnd=1404862769035
        #http://weibo.com/p/aj/mblog/mbloglist?_wv=5&domain=100206&pre_page=3&page=3&count=15&pagebar=0&id=1002062093492691
        #http://weibo.com/p/aj/mblog/mbloglist?domain=100206&pre_page=3&page=3&pagebar=0&id=1002062093492691
        #http://weibo.com/p/aj/mblog/mbloglist?domain=100206&pre_page=3&page=3&id=1002062093492691
        #domain 
        #page_id
        url = 'http://weibo.com/p/aj/mblog/mbloglist?domain=%s&pre_page=%d&page=%d&id=%s&pagebar=%d' % (self.domain, page, page, self.id, self.pagebar)
        request = urllib2.Request(url, None, self.req_header)
        resp = urllib2.urlopen(request)
        decodeStr = json.loads(resp.read())
        html = decodeStr['data']
        #logging.debug(html)
        
        self.Analyze(html)

        self.pagebar = self.pagebar + 1

    def Analyze(self, content):
        soup = BeautifulSoup(content)
        wbs = soup.find_all('div', {'class':'WB_detail'})
        wbt = soup.find_all('div', {'class':'WB_from'})
        for i, wb in enumerate(wbs):
            tag = wb.find('div', {'class':'WB_text', 'node-type':'feed_list_content'})

            weiboText = tag.get_text().strip()
            tag = wb.find('div', {'class':'WB_text', 'node-type':'feed_list_reason'})
            if tag:
                #logging.debug('REASON:' + tag.get_text().strip())
                pass
            if wbt[i]:
                tag = wbt[i].find('a', {'node-type':'feed_list_item_date'})
                if tag:
                    posttime = tag.get('title')

            logging.debug('[%s]%s' % (posttime, weiboText))

    def RequestHot(self):
        url = 'http://hot.weibo.com/'

        request = urllib2.Request(url, None, self.req_header)
        resp = urllib2.urlopen(request)

        html = resp.read()
        #logging.debug(html)
        mids = []

        soup = BeautifulSoup(html)
        wbs = soup.find_all('div', {'class':'WB_detail'})
        for i, wb in enumerate(wbs):
            tag = wb.find('div', {'class':'WB_text', 'node-type':'feed_list_content'})
            weiboText = tag.get_text().strip()
            logging.debug(weiboText)
            #action-type="feed_list_forward"
            forward = wb.find('a', {'action-type':'feed_list_forward'})
            forwardText = forward.get('action-data')
            logging.debug(forwardText)

            mid = ''
            for part in forwardText.split('&'):
                fv = part.split('=')
                if fv[0] == 'mid':
                    mid = fv[1]
            mids.append(mid)
        return mids
            

    def Forward(self, mid, text):
        data = {'category': '9999',
                'soururl' : '',
                'mid' : mid,
                'srvid' : '',
                '_t' : '0',
                'reason' : text.encode('utf-8')
        }

        forwardURL = 'http://hot.weibo.com/ajax/addone'

        req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2015.0 Safari/537.36',
                      'Accept':'*/*',
                      'Accept-Language':'en-US,en;q=0.8,it;q=0.6,ja;q=0.4,zh-CN;q=0.2,zh-TW;q=0.2',
                      'Referer':'http://hot.weibo.com/'
                      }

        request = urllib2.Request(forwardURL, urllib.urlencode(data), req_header)
        resp = urllib2.urlopen(request)

    def Post(self, text):
        data = {'text': text,
                'pic_id' : '',
                'rank' : '0',
                'rankid' : '',
                'location' : '0',
                'module' : 'topquick'
        }
        

        postURL = 'http://www.weibo.com/aj/mblog/add?_wv=5'

        req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2015.0 Safari/537.36',
                      'Accept':'*/*',
                      'Accept-Language':'en-US,en;q=0.8,it;q=0.6,ja;q=0.4,zh-CN;q=0.2,zh-TW;q=0.2',
                      'Referer':'http://www.weibo.com/minipublish?uid=%s' % (self.uid)
                      }

        request = urllib2.Request(postURL, urllib.urlencode(data), req_header)
        resp = urllib2.urlopen(request)

        logging.debug(resp.read())


    def get_pwd(self, password, servertime, nonce, pubkey):
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537) #创建公钥
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(password) #拼接明文js加密文件中得到
        passwd = rsa.encrypt(message, key) #加密
        passwd = binascii.b2a_hex(passwd) #将加密信息转换为16进制。
        return passwd


def main():
    test_hot()

def test_hot():
    weibo = Weibo()
    weibo.Login()
    for mid in weibo.RequestHot():
        weibo.Forward(mid, FORWARD[random.randint(0,len(FORWARD)-1)])
        time.sleep(10 + random.randint(1,10))
        print 'Waiting...'

def test_post():
    myURL = 'http://weibo.com/cnwarden'  #my web
    weibo = Weibo()
    weibo.Login()
    weibo.PrepareRequest(myURL)
    i = 0
    while True:
        i = i + 1
        weibo.Post('ChinaHere!!!%d' % (i))
        time.sleep(10)

def test_gather():
    baseURL = 'http://www.weibo.com/p/1006061823348853'
    weibo = Weibo()
    weibo.Login()
    weibo.PrepareRequest(baseURL)
    for i in range(1,5):
        print 'Processing Page[%d]' % (i)
        weibo.Request(weibo.GetPageURL(i))
        weibo.RequestWithScroll(i)
        weibo.RequestWithScroll(i)

if __name__ == '__main__':
    main()

