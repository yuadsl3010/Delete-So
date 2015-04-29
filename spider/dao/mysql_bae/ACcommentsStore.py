#!/usr/bin/python
#coding=utf8

import MySQLdb

class ACcommentsStore(object):
    '''
投稿信息表各项操作
    '''
    __dbinfo = "";

    def __init__(self, dbinfo):
        self.__dbinfo = dbinfo;
        
    def insert(self, data):
        try:
            conn = MySQLdb.connect(host = self.__dbinfo.get_host(), \
                                    port = self.__dbinfo.get_port(), \
                                    user = self.__dbinfo.get_user(), \
                                    passwd = self.__dbinfo.get_pwd(), \
                                    db = self.__dbinfo.get_dbname(), \
                                    charset = self.__dbinfo.get_charset());
            cursor = conn.cursor();
            for j, k in enumerate(data):
                try:
                    cursor.execute("DELETE FROM accommentsstore WHERE cid = %s", (k.get_cid()));
                    break;
                except Exception as e:
                    pass;#print("未知错误: ", e);
                
            for j, k in enumerate(data):
                try:
                    cursor.execute("INSERT INTO accommentsstore(cid, name, content) VALUES(%s, %s, %s)", \
                                      (k.get_cid(), \
                                       k.get_name(), \
                                       k.get_content()));
                except Exception as e:
                    pass;#print("未知错误: ", e);
            
            cursor.close();
            conn.commit();
            conn.close();
        except Exception as e:
            pass;#print("未知错误: ", e);

    def clear(self, cids):
        try:
            conn = MySQLdb.connect(host = self.__dbinfo.get_host(), \
                                    port = self.__dbinfo.get_port(), \
                                    user = self.__dbinfo.get_user(), \
                                    passwd = self.__dbinfo.get_pwd(), \
                                    db = self.__dbinfo.get_dbname(), \
                                    charset = self.__dbinfo.get_charset());
            cursor = conn.cursor();
            for j, k in enumerate(cids):
                try:
                    cursor.execute("DELETE FROM accommentsstore WHERE cid = %s LIMIT 1000", (k));
                except Exception as e:
                    print("未知错误: ", e);
            
            
            cursor.close();
            conn.commit();
            conn.close();
        except Exception as e:
            pass;#print("未知错误: ", e);