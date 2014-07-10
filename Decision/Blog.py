# -*- coding: utf-8 -*-



import urllib2
import logging
import re
import sys
import os
import codecs
from bs4 import BeautifulSoup
from datetime import datetime

'''
subpage:
example:http://blog.sina.com.cn/s/article_sort_1594987341_10001_2.html
page = 
'''

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

class BlogFilter(object):
    """docstring for BlogFilter"""
    def __init__(self):
        super(BlogFilter, self).__init__()

    def SetTimeRange(self, start, end):
        self.start = start
        self.end = end

    def DoFilter(self, item):
        if hasattr(item, 'timestamp'):
            if item.timestamp > self.start and item.timestamp < self.end:
                return True
        return False


class Blog(object):
    """docstring for Blog"""
    def __init__(self):
        super(Blog, self).__init__()
        self.links = []
        self.blogId = ''
        self.filter = BlogFilter()
        self.filter.SetTimeRange(datetime(2014,7,8), datetime(2014,7,9))
        self.BASE_FOLDER = './blog/'
        if not os.path.exists(self.BASE_FOLDER):
                os.mkdir(self.BASE_FOLDER)
        #init urllib2
        proxyHandler = urllib2.ProxyHandler({'http':'http://10.40.14.56:8080'})
        opener = urllib2.build_opener(proxyHandler)
        urllib2.install_opener(opener)

    def Add(self, link):
        self.links.append(link)

    def Get(self):
        for link in self.links:
            self.GetPageInfo(link)
            self.GetArticleList()

    def GetPageInfo(self, blog):

        logging.debug('start extracting the message!')

        response = urllib2.urlopen(blog)

        re = response.read()
        response.close()

        soup = BeautifulSoup(self.__tidy__(re))
        tag = soup.find('div', {'class':'SG_page'})
        if tag:
            self.pageNav = tag.get('id')
            self.pageNum = int(tag.get('total')) / int(tag.get('pagesize'))
            logging.debug(self.pageNav) #pagination_10001
            logging.debug(self.pageNum)


        logging.debug('stop extracting the blog:')

    def GetArticleList(self):
        #http://blog.sina.com.cn/s/article_sort_1594987341_10001_2.html
        #removing pagination_ from pageNav
        pageNav = self.pageNav.find('_')
        for page in range(1, self.pageNum): #
            print 'Processing Page[%d]' % (page)
            url = 'http://blog.sina.com.cn/s/article_sort_%s_%s_%d.html' % (self.blogId, self.pageNav[pageNav+1:], page)
            logging.debug(url)

            response = urllib2.urlopen(url)
            re = response.read()
            response.close()

            data = []
            soup = BeautifulSoup(self.__tidy__(re))

            #create folder
            if not os.path.exists(self.BASE_FOLDER + self.blogId):
                os.mkdir(self.BASE_FOLDER + self.blogId)

            tags = soup.find_all('div', {'class':'blog_title'})
            time_tags = soup.find_all('span', {'class':'time SG_txtc'})
            
            if tags and time_tags and len(tags) == len(time_tags):
                for i, item in enumerate(tags):
                    tt = tags[i].find('a')
                    time = time_tags[i].get_text()
                    time = time.replace('(', '').replace(')','')
                    timestamp = datetime.strptime(time, '%Y-%m-%d %H:%M')
                    #logging.debug(date)
                    data.append((tt.get('href'), tt.get_text(), timestamp))

            #logging.debug(data)
            for item in data:
                logging.debug('LINK:%s TITLE:%s' % (item[0], item[1]))
                print '---Processing subpage[%s]' % (item[0])
                self.timestamp = timestamp
                if self.filter.DoFilter(self):
                    self.GetArticle(item[0], item[1], item[2])
                else:
                    logging.debug('Filtered:%s' % (item[0]))
                    return # DONE
                    

    def Index(self, url, title, timestamp):
        #<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        filename = '%s/index.htm' % (self.BASE_FOLDER+self.blogId)
        writeHeader = False
        if not os.path.exists(filename):
            writeHeader = True

        fp = codecs.open(filename, 'a', encoding='utf-8')
        if writeHeader:
            fp.write(r'<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /></head>')
        fp.write('<a href="%s">%s-%s</a><br/>' % (url, timestamp.strftime('%Y-%m-%d'), title))
        fp.close()

    def SavePage(self, pageName, content):
        filename = '%s/%s' % (self.BASE_FOLDER+self.blogId, pageName)
        fp = codecs.open(filename, 'w', encoding='utf-8')
        fp.write(r'<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /></head>')
        fp.write(content)
        fp.close()

    def GetArticle(self, url, title, timestamp):
        #<div id="sina_keyword_ad_area2" class="articalContent   newfont_family">
        #<span class="time SG_txtc">(2014-06-27 15:43:01)</span>
        pageName = url[url.rfind('blog_'):]
        self.Index(pageName, title, timestamp)

        response = urllib2.urlopen(url)
        re = response.read()
        response.close()

        soup = BeautifulSoup(self.__tidy__(re))

        #content
        tag = soup.find('div', {'class':'articalContent   newfont_family'})
        if tag:
            #logging.debug(tag.get_text())
            self.SavePage(pageName, tag.get_text())
            pass
        else:
            tag = soup.find('div', {'class':'articalContent   '})
            if tag:
                #logging.debug(tag.get_text())
                self.SavePage(pageName, tag.get_text())
                pass
            else:
                logging.debug('Content Failed')
                pass

    def __tidy__(self, str):
        outputstr = ''
        for line in str.split('\r\n'):
            if re.search('<meta.*' , line):
                pass
            elif re.search('http://blog.sina.com.cn/s/articlelist_(\d*)_0_1.html', line):
                m = re.search('http://blog.sina.com.cn/s/articlelist_(\d*)_0_1.html', line)
                self.blogId = m.group(1)
            else:
                outputstr = outputstr + line
        #logging.debug(outputstr)
        return outputstr


def main():
    blog = Blog()
    blog.Add('http://blog.sina.com.cn/gmlz2009')
    blog.Add('http://blog.sina.com.cn/u/1773146721')
    blog.Add('http://blog.sina.com.cn/u/1671224202')
    blog.Add('http://blog.sina.com.cn/u/1983538704')
    blog.Add('http://blog.sina.com.cn/u/1671224202')
    blog.Add('http://blog.sina.com.cn/u/1278127565')
    blog.Get()


if __name__ == '__main__':
    main()

