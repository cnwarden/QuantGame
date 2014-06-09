#-*- coding:utf-8 -*-

import sys
import os
import wx
from Frame.FrameMain import FrameMain

sys.path.append(r'Plugins')

print sys.path

class QuantApp(wx.App):
    def __init__(self):
        wx.App.__init__(self)
        frame = FrameMain(u'QuantGame')
        frame.Show()


def main():
    app = QuantApp()
    app.MainLoop()



if __name__ == '__main__':
    main()