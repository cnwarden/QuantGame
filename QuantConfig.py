#-*- coding:utf-8 -*-

import sys
import os
import ConfigParser

class QuantConfig():

    def __init__(self):
        self.cfg = ConfigParser.ConfigParser()
        self.cfg.read('FreeQuant.ini')

    def IsEnabledProxy(self):
        Enabled = int(self.cfg.get('Network','EnableProxy'))

        return Enabled

    def GetProxyConfig(self):
        proxyIp = self.cfg.get('Network','ProxyIP')
        proxyPort = self.cfg.get('Network', 'ProxyPort')

        return proxyIp, proxyPort



def main():
    cfg = QuantConfig()
    print cfg.GetProxyConfig()



if __name__ == '__main__':
    main()