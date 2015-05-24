#!/usr/bin/python
#coding=utf8

import MySQLdb

class ACcommentsStatus(object):
    '''
AC状态记录
    '''
    __dbinfo = "";

    def __init__(self, dbinfo):
        self.__dbinfo = dbinfo;
        
    def log(self, data):
        try:
            conn = MySQLdb.connect(host = self.__dbinfo.get_host(), \
                                    port = self.__dbinfo.get_port(), \
                                    user = self.__dbinfo.get_user(), \
                                    passwd = self.__dbinfo.get_pwd(), \
                                    db = self.__dbinfo.get_dbname(), \
                                    charset = self.__dbinfo.get_charset());
            cursor = conn.cursor();
            try:
                if data == "acfunstart":
                    cursor.execute("UPDATE status SET status = NOW() WHERE name = 'acfunstart'");
                elif data == "acfunend":
                    cursor.execute("UPDATE status SET status = NOW() WHERE name = 'acfunend'");
                elif data == "acrefresh":
                    cursor.execute("UPDATE status SET status = NOW() WHERE name = 'acrefresh'");
            except Exception as e:
                pass;#print("未知错误: ", e);
            
            cursor.close();
            conn.commit();
            conn.close();        
        except Exception as e:
            pass;
        
    def score(self, data):
        try:
            conn = MySQLdb.connect(host = self.__dbinfo.get_host(), \
                                    port = self.__dbinfo.get_port(), \
                                    user = self.__dbinfo.get_user(), \
                                    passwd = self.__dbinfo.get_pwd(), \
                                    db = self.__dbinfo.get_dbname(), \
                                    charset = self.__dbinfo.get_charset());
            cursor = conn.cursor();
            try:
                cursor.execute("UPDATE status SET status = NOW(), score = %s WHERE name = 'acscore'", data);
            except Exception as e:
                pass;#print("未知错误: ", e);
            
            cursor.close();
            conn.commit();
            conn.close();        
        except Exception as e:
            pass;