#-*- coding:utf-8 -*-

#----------------------------------------------------------------------------
# Name:        News Windows
# Purpose:     Display News
#
# Author:      Ming He
#
# Created:     11-Jun-2014
#----------------------------------------------------------------------------
# 06/11/2014 - Ming.He (cnwarden@gmail.com)
#

import wx
import sys
import subprocess

class FrameNews(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, -1, title, size=(600,400))

        self.list = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        
        self.list.InsertColumn(0, u'新闻链接')
        self.list.InsertColumn(1, u'新闻标题')
        

        self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnDClick)

    def ShowData(self, data):
        for idx, item in enumerate(data):
            #item = wx.ListItem()
            #item.SetText(item[0])
            #self.list.InsertItem(item)
            self.list.InsertStringItem(sys.maxint, item[0])
            self.list.SetStringItem(idx, 1, item[1])

        self.list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.Show()

    def OnDClick(self, event):
        link = event.GetItem().GetText()
        subprocess.call([r'C:\Program Files (x86)\Internet Explorer\iexplore.exe',link])


    def OnContextMenu(self, event):
        print 'onxtextmenu'
        menu = wx.Menu()

        item1 = wx.MenuItem(menu, wx.NewId(), '&Open')
        menu.AppendItem(item1)

        self.PopupMenu(menu)

        menu.Destory()


def main():

    app = wx.PySimpleApp()
    frame = FrameNews(u'浦东银行')
    data = [('abc','ddd'), ('ccc', 'ddd')]
    frame.ShowData(data)
    app.MainLoop()



if __name__ == '__main__':
    main()