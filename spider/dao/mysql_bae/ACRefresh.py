#!/usr/bin/python
#coding=utf8

import MySQLdb

class ACRefresh(object):
    '''
投稿信息表各项操作
    '''
    __dbinfo = "";

    def __init__(self, dbinfo):
        self.__dbinfo = dbinfo;
        
    def get(self):
        results = []
        
        try:
            conn = MySQLdb.connect(host = self.__dbinfo.get_host(), \
                                    port = self.__dbinfo.get_port(), \
                                    user = self.__dbinfo.get_user(), \
                                    passwd = self.__dbinfo.get_pwd(), \
                                    db = self.__dbinfo.get_dbname(), \
                                    charset = self.__dbinfo.get_charset());
            cursor = conn.cursor();
            try:
                cursor.execute("SELECT * FROM acrefresh WHERE id != 0");
                results = cursor.fetchall()
            except Exception as e:
                print(e);
            
            cursor.close();
            conn.commit();
            conn.close();
        except Exception as e:
            print(e);
        
        return results
        
    def update(self, data):
        try:
            conn = MySQLdb.connect(host = self.__dbinfo.get_host(), \
                                    port = self.__dbinfo.get_port(), \
                                    user = self.__dbinfo.get_user(), \
                                    passwd = self.__dbinfo.get_pwd(), \
                                    db = self.__dbinfo.get_dbname(), \
                                    charset = self.__dbinfo.get_charset());
            cursor = conn.cursor();
            
            for index, item in enumerate(data):
                try:
                    cursor.execute("UPDATE acrefresh SET status = %s WHERE id = %s", \
                                      (item.get_status(), \
                                       item.get_id()));
                except Exception as e:
                    continue
            
            cursor.close();
            conn.commit();
            conn.close();
        except Exception as e:
            print(e);

    def delete(self, data):
        try:
            conn = MySQLdb.connect(host = self.__dbinfo.get_host(), \
                                    port = self.__dbinfo.get_port(), \
                                    user = self.__dbinfo.get_user(), \
                                    passwd = self.__dbinfo.get_pwd(), \
                                    db = self.__dbinfo.get_dbname(), \
                                    charset = self.__dbinfo.get_charset());
            cursor = conn.cursor();
            for index, item in enumerate(data):
                try:
                    cursor.execute("DELETE FROM acrefresh WHERE id = %s", item);
                except Exception as e:
                    continue
            
            cursor.close();
            conn.commit();
            conn.close();
        except Exception as e:
            print(e);