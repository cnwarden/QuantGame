#-*- coding:utf-8 -*-

'''
Refer To SINA API
http://mizarrr.blog.163.com/blog/static/1651594112011101882538362/

http://market.finance.sina.com.cn/downxls.php?date=2011-07-08&symbol=sh600900
获取代码为sh600900，在2011-07-08的成交明细，数据为xls格式。
http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_price.php?symbol=sh600900
获得sh600900当日的分价表
http://market.finance.sina.com.cn/pricehis.php?symbol=sh600900&startdate=2011-08-17&enddate=2011-08-19
获得sh600900从2011-08-17到2011-08-19的分价表。
以大秦铁路（股票代码：601006）为例，如果要获取它的最新行情，只需访问新浪的股票数据
接口：http://hq.sinajs.cn/list=sh601006这个url会返回一串文本，例如：
var hq_str_sh601006="大秦铁路, 27.55, 27.25, 26.91, 27.55, 26.20, 26.91, 26.92,
22114263, 589824680, 4695, 26.91, 57590, 26.90, 14700, 26.89, 14300,
26.88, 15100, 26.87, 3100, 26.92, 8900, 26.93, 14230, 26.94, 25150, 26.95, 15220, 26.96, 2008-01-11, 15:05:32";
这个字符串由许多数据拼接在一起，不同含义的数据用逗号隔开了，按照程序员的思路，顺序号从0开始。
0：”大秦铁路”，股票名字；
1：”27.55″，今日开盘价；
2：”27.25″，昨日收盘价；
3：”26.91″，当前价格；
4：”27.55″，今日最高价；
5：”26.20″，今日最低价；
6：”26.91″，竞买价，即“买一”报价；
7：”26.92″，竞卖价，即“卖一”报价；
8：”22114263″，成交的股票数，由于股票交易以一百股为基本单位，所以在使用时，通常把该值除以一百；
9：”589824680″，成交金额，单位为“元”，为了一目了然，通常以“万元”为成交金额的单位，所以通常把该值除以一万；
10：”4695″，“买一”申请4695股，即47手；
11：”26.91″，“买一”报价；
12：”57590″，“买二”
13：”26.90″，“买二”
14：”14700″，“买三”
15：”26.89″，“买三”
16：”14300″，“买四”
17：”26.88″，“买四”
18：”15100″，“买五”
19：”26.87″，“买五”
20：”3100″，“卖一”申报3100股，即31手；
21：”26.92″，“卖一”报价
(22, 23), (24, 25), (26,27), (28, 29)分别为“卖二”至“卖四的情况”
30：”2008-01-11″，日期；
31：”15:05:32″，时间；

对于股票的K线图，日线图等的获取可以通过请求http://image.sinajs.cn/…./…/*.gif此URL获取，其中*代表股票代码，详见如下：
查看日K线图：
http://image.sinajs.cn/newchart/daily/n/sh601006.gif
分时线的查询：
http://image.sinajs.cn/newchart/min/n/sh000001.gif
日K线查询：
http://image.sinajs.cn/newchart/daily/n/sh000001.gif
周K线查询：
http://image.sinajs.cn/newchart/weekly/n/sh000001.gif
月K线查询：
http://image.sinajs.cn/newchart/monthly/n/sh000001.gif
'''

import urllib2
import codecs
from bs4 import BeautifulSoup
import wx
import sys
from QuantConfig import QuantConfig

class SinaDAO:


    def __init__(self):

        cfg = QuantConfig()
        if cfg.IsEnabledProxy():
            proxyHandler = urllib2.ProxyHandler({'http':'http://%s:%s' % (cfg.GetProxyConfig())})
            opener = urllib2.build_opener(proxyHandler)
            urllib2.install_opener(opener)


    def getHistory(self, instrumentId):
        reqStr = 'http://market.finance.sina.com.cn/downxls.php?date=2011-07-08&symbol=sh%s'

        re = urllib2.urlopen(reqStr % (instrumentId))

        print re.read()

    def getLastTick(self, instrumentId):
        reqStr = 'http://hq.sinajs.cn/list=sh%s'

        re = urllib2.urlopen(reqStr % (instrumentId))

        print re.read()

    def getIndex(self, indexId):
        reqStr = 'http://hq.sinajs.cn/list=s_sh%s'

        re = urllib2.urlopen(reqStr % (indexId))

        print re.read()

    def getNews(self, instrumentId):

        reqStr = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllNewsStock/symbol/sh%s.phtml'
        re = urllib2.urlopen(reqStr % (instrumentId))

        data = []
        soup = BeautifulSoup(re.read())
        tag = soup.find('div', {'class':'datelist'})
        for tt in tag.find_all('a'):
            data.append((tt.get('href'), tt.get_text()))
        return data
        
    def TestURL(self, instrumentId):
        '''
        news:http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllNewsStock/symbol/sh600900.phtml
        '''
        reqStr = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllNewsStock/symbol/sh600900.phtml'

        fp = codecs.open('C:\\test.txt', 'w', 'utf-8')

        re = urllib2.urlopen(reqStr)

        data = []

        soup = BeautifulSoup(re.read())
        tag = soup.find('div', {'class':'datelist'})
        print type(tag)
        for tt in tag.find_all('a'):
            fp.write( "%s|%s\n" % (tt.get('href'), tt.get_text()))
            data.append((tt.get('href'), tt.get_text()))

        fp.close()
        return data


class DemoFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "600000", size=(600,400))

        self.list = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.list.InsertColumn(0, u'新闻链接')
        self.list.InsertColumn(1, u'新闻标题')
        

    def ShowData(self, data):
        for idx, item in enumerate(data):
            self.list.InsertStringItem(sys.maxint, item[0])
            self.list.SetStringItem(idx, 1, item[1])

        self.list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        
        self.Show()


    def OnContextMenu(self, event):
        menu = wx.Menu()

        item1 = wx.MenuItem(menu, 1, '&Open')
        menu.AppendItem(item1)

        self.PopupMenu(menu)

        menu.Destory()


def main():
    print 'Testing Sina DAO'
    dao = SinaDAO()
    #dao.getHistory('600000')
    #dao.getLastTick('600000')
    #dao.getIndex('000001')
    #data = dao.TestURL('600000')

    app = wx.PySimpleApp()
    frame = DemoFrame()
    frame.ShowData(dao.getNews('600000'))
    app.MainLoop()



if __name__ == '__main__':
    main()