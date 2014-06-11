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
import re as regex
from xml.dom import minidom

sys.stdout = codecs.open('.\\log.txt','w', encoding='UTF-8')

PLUGIN_NAME=u'参考数据'

def OnLoad(baseFrame):
    print 'OnLoad'
    
def OnUnLoad(baseFrame):
    print 'Unload'

def FormatJson(data):
    p = regex.compile(r'\\(?![/u"])')
    fixed = p.sub(r"\\\\", data)
    return fixed

def FormatJsonStock(data):
    p = regex.compile(r',(\w)')
    fixed = p.sub(r',"\1', data)
    p1 = regex.compile(r',"(\w*?):')
    fixed1 = p1.sub(r',"\1":', fixed)
    p2 = regex.compile(r'symbol')
    fixed2 = p2.sub(r'"symbol"', fixed1)
    return fixed2
    
    
def Run(event):
    print 'Run'
    #proxyHandler = urllib2.ProxyHandler({'http':'http://10.40.14.56:8080'})
    #opener = urllib2.build_opener(proxyHandler)
    #urllib2.install_opener(opener)

    re = urllib2.urlopen('http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodes')
    data = u''
    data = re.read().decode('GB2312')
    jsonObj = json.loads(FormatJson(data))
    #fp.write(data)
    #print len(jsonObj)
    #print len(jsonObj[1])
    #层级目录-新浪行业

    doc = minidom.Document()
    doc.appendChild(doc.createComment('Stock List From Sina'))
    stockList = doc.createElement('stocklist')
    doc.appendChild(stockList)

    for i, item in enumerate(jsonObj[1][0][1][1][1]):
        if i > 10:
            break
        print '%s-%s' % (item[0], item[2])
        #Count
        re = urllib2.urlopen('http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCount?node=%s' % (item[2]))
        data = re.read().decode('GB2312')
        m = regex.search("\"(.*)\"", data)
        numOfItems = 0
        if m:
            numOfItems = int(m.group(1))

        #Get all items in one page
        re = urllib2.urlopen('http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=%d&sort=symbol&asc=1&node=%s&symbol=&_s_r_a=init' % (numOfItems, item[2]))
        data = re.read().decode('GB2312')

        stockObjs = json.loads(FormatJsonStock(data))

        try:
            if stockObjs:
                for i, stock in enumerate(stockObjs):
                        node = doc.createElement('stock')
                        node.setAttribute("id", stock["code"])
                        node.setAttribute("name", stock["name"])
                        tagNode = doc.createElement('tag')
                        tagNode.appendChild(doc.createTextNode(item[0]))
                        node.appendChild(tagNode)
                        stockList.appendChild(node)
        except Exception,e:
            print e    

    f = codecs.open('.\\stock.xml','w', encoding='UTF-8')
    doc.writexml(f)
    f.close()


if __name__ == '__main__':
    Run(None)