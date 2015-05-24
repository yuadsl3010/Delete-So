#!/usr/bin/python
#coding=utf8

import socket
import urllib2
from base.Constants import *

class urlWork(object):
    '''
这个类是用来完成URL各种操作的。
    '''
    def sendGet(self, url):
        '''
          这个类是用来发送URL请求的。
        '''
        content = "";
        timeout = 5;
        socket.setdefaulttimeout(timeout);
        
        try:
            data = urllib2.urlopen(url);
            content = data.read().decode("utf-8");
        except Exception:  
            return URL_EXCEPTION;
            
        return content;