#-*- coding:utf-8 -*-

import wx
import sys

class FrameNews(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, -1, title, size=(600,400))

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