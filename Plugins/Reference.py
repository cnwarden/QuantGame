#-*- coding:utf-8 -*-
'''
http://stock.finance.sina.com.cn/yuanchuang/api/jsonp.json

http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodes

http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCount?node=new_swzz

http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=40&sort=symbol&asc=1&node=new_swzz&symbol=&_s_r_a=init

'''

import sys
import json
import urllib2
import codecs

PLUGIN_NAME=u'参考数据'

def OnLoad(baseFrame):
    print 'OnLoad'
    
def OnUnLoad(baseFrame):
    print 'Unload'
    
def Run(event):
    print 'Run'
    #cfg = QuantConfig()
    #if cfg.IsEnabledProxy():
    #    proxyHandler = urllib2.ProxyHandler({'http':'http://%s:%s' % (cfg.GetProxyConfig())})
    #    opener = urllib2.build_opener(proxyHandler)
    #    urllib2.install_opener(opener)

    fp = codecs.open('C:\\test.txt','w', encoding='utf-8')
    re = urllib2.urlopen('http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodes')
    data = u''
    data = re.read().decode('GB2312')
    fp.write(data)

    re = urllib2.urlopen('http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCount?node=new_swzz')
    data = re.read().decode('GB2312')
    fp.write(data)

    re = urllib2.urlopen('http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=40&sort=symbol&asc=1&node=new_swzz&symbol=&_s_r_a=init')
    data = re.read().decode('GB2312')
    fp.write(data)

    fp.close()

if __name__ == '__main__':
    Run(None)
