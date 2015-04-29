#coding=utf8

from dao.mysql_normal.ACcomments import *
from dao.mysql_normal.ACcommentsInfo import *
from dao.mysql_normal.ACcommentsStore import *

class ACdaoMysqlNormal(object):
    '''
    本地mysql数据库的适配
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
        