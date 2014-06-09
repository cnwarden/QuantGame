#-*- coding:utf-8 -*-

import os
import wx
import wx.lib.customtreectrl as CTL
import sys
from FrameNews import FrameNews
from DataAccess.SinaDAO import SinaDAO

class FrameMain(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, -1, title, size=(600,400))

        self.statusBar = self.CreateStatusBar()
        self.menuBar = wx.MenuBar()

        menu1 = wx.Menu()
        self.menuFileNew = menu1.Append(wx.NewId(), u'创建文件', u'创建一个新文件')
        self.menuFileOpen = menu1.Append(wx.NewId(), u'打开文件', u'打开一个存在的文件')
        self.menuBar.Append(menu1, u'文件')

        menu2 = wx.Menu()
        self.menuSourceSina = menu2.Append(wx.NewId(), u'新浪财经', u'使用新浪财经')
        self.menuSourceNetease = menu2.Append(wx.NewId(), u'网易财经', u'使用网易财经')
        self.menuBar.Append(menu2, u'数据源')

        menu3 = wx.Menu()
        #menu3.Append(wx.NewId(), u'新浪财经', u'使用新浪财经')
        #menu3.Append(wx.NewId(), u'网易财经', u'使用网易财经')
        self.menuBar.Append(menu3, u'插件')

        menu4 = wx.Menu()
        self.menuBar.Append(menu4, u'工具')
        menu4.Append(wx.NewId(), u'设置', u'配置更改')

        menu5 = wx.Menu()
        self.menuBar.Append(menu5, u'关于')
        
        self.SetMenuBar(self.menuBar)

        self.Bind(wx.EVT_MENU,self.OnFileNew,self.menuFileNew)
        self.Bind(wx.EVT_MENU,self.OnFileOpen,self.menuFileOpen)

        self.Bind(wx.EVT_MENU,self.OnSourceChanged,self.menuSourceSina)
        self.Bind(wx.EVT_MENU,self.OnSourceChanged,self.menuSourceNetease)

        ################################

        self.treeList = CTL.CustomTreeCtrl(self)

        root = self.treeList.AddRoot(u'上证交易所')
        self.treeList.AppendItem(root, u'浦发银行').SetData('600000')
        self.treeList.AppendItem(root, u'兴发银行').SetData('600001')
        self.treeList.Expand(root)

        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED,self.OnTreeDoubleClick)

        for plugin in self.LoadPlugins():
            menuItem = menu3.Append(wx.NewId(), plugin[0])
            self.Bind(wx.EVT_MENU,plugin[2],menuItem)

    def LoadPlugins(self):
        """
        call the interface OnLoad
        """
        plugin_info = []
        for file in os.listdir(r'Plugins'):
            if(file.endswith('py')):
                p = __import__(file[:-3])
                name = getattr(p, 'PLUGIN_NAME')
                onloadFun = getattr(p, 'OnLoad')
                runFun = getattr(p, 'Run')
                plugin_info.append([name, onloadFun, runFun])

        return plugin_info

    def OnContextMenu(self, event):
        pass

    def OnFileNew(self, event):
        print 'new file'
        pass

    def OnFileOpen(self, event):
        print 'open file'
        pass

    def OnSourceChanged(self, event):
        print 'source changed'
        pass

    def OnTreeDoubleClick(self, event):
        print event.GetItem().GetData()
        event.GetItem().SetBold(True)
        frame = FrameNews(event.GetItem().GetData())
        dao = SinaDAO()
        frame.ShowData(dao.getNews(event.GetItem().GetData()))


def main():
    app = wx.PySimpleApp()
    frame = FrameMain(u'QuantGame')
    frame.Show()
    app.MainLoop()



if __name__ == '__main__':
    main()