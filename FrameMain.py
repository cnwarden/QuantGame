#-*- coding:utf-8 -*-

import os
import wx
import wx.lib.customtreectrl as CTL
import wx.lib.agw.aui as aui
import wx.lib.splitter as splitter

import sys
from xml.dom import minidom
from FrameNews import FrameNews
from SinaDAO   import SinaDAO

class TabPanelOne(wx.Panel):
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        sizer = wx.BoxSizer(wx.VERTICAL)
        txtOne = wx.TextCtrl(self, wx.ID_ANY, "")
        txtTwo = wx.TextCtrl(self, wx.ID_ANY, "")
        sizer.Add(txtOne, 0, wx.ALL, 5)
        sizer.Add(txtTwo, 0, wx.ALL, 5)
        self.SetSizer(sizer)

class FrameMain(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, -1, title, size=(600,400))

        splitWindow = splitter.MultiSplitterWindow(self, wx.ID_ANY)
        
        #left treelist
        self.treeList = CTL.CustomTreeCtrl(splitWindow)
        root = self.treeList.AddRoot(u'上证交易所')
        for instrument in self.LoadInstruments():
            self.treeList.AppendItem(root, instrument[0]).SetData(instrument[1])
        self.treeList.Expand(root)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED,self.OnTreeDoubleClick)

        splitWindow.AppendWindow(self.treeList)


        #import AUI
        self._mgr = aui.AuiManager()
        self._mgr.SetManagedWindow(splitWindow)

        notebook = aui.AuiNotebook(splitWindow)
        panelOne = TabPanelOne(notebook)
        panelTwo = TabPanelOne(notebook)

        notebook.AddPage(panelOne, u"历史数据", False)
        notebook.AddPage(panelTwo, u"图表", False)

        self._mgr.AddPane(notebook, aui.AuiPaneInfo().Name('content').CenterPane().PaneBorder(False))
        self._mgr.Update()
        
        splitWindow.AppendWindow(notebook)

        self.statusBar = self.CreateStatusBar()
        self.menuBar = self.CreateMenu()

        

    def CreateMenu(self):
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

        for plugin in self.LoadPlugins():
            menuItem = menu3.Append(wx.NewId(), plugin[0])
            self.Bind(wx.EVT_MENU,plugin[2],menuItem)

    def LoadInstruments(self):
        InstrumentList = []
        doc = minidom.parse('.\\Data\\stock.xml')
        for node in doc.getElementsByTagName('stock'):
            InstrumentList.append((node.getAttribute('name'),node.getAttribute('id')))
        return InstrumentList

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
    frame.LoadInstruments()
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()