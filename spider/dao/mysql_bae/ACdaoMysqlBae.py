#!/usr/bin/python
#coding=utf8

from dao.mysql_bae.ACcomments import *
from dao.mysql_bae.ACcommentsInfo import *
from dao.mysql_bae.ACcommentsStore import *
from dao.mysql_bae.ACcommentsStatus import *
from dao.mysql_bae.ACRefresh import *

class ACdaoMysqlBae(object):
    '''
    百度云mysql数据库的适配
    '''
    __dbinfo = "";

    def __init__(self, dbinfo):
        self.__dbinfo = dbinfo;
        
    def getACCommentsInfo(self):
        return ACcommentsInfo(self.__dbinfo);
    
    def getACComments(self):
        return ACcomments(self.__dbinfo);
    
    def getACCommentsStore(self):
        return ACcommentsStore(self.__dbinfo);

    def getACCommentsStatus(self):
        return ACcommentsStatus(self.__dbinfo);
    
    def getACRefresh(self):
        return ACRefresh(self.__dbinfo);
        