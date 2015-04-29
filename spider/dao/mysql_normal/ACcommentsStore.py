#coding=utf8

from pymysql.err import *
import pymysql

class ACcommentsStore(object):
    '''
投稿信息表各项操作
    '''
    __dbinfo = "";

    def __init__(self, dbinfo):
        self.__dbinfo = dbinfo;
        
    def insert(self, data):
        conn = pymysql.connect(host = self.__dbinfo.get_host(), \
                                    port = self.__dbinfo.get_port(), \
                                    user = self.__dbinfo.get_user(), \
                                    passwd = self.__dbinfo.get_pwd(), \
                                    db = self.__dbinfo.get_dbname(), \
                                    charset = self.__dbinfo.get_charset());
        cursor = conn.cursor();
        print("store start...");
        for j, k in enumerate(data):
            try:
                cursor.execute("DELETE FROM ACcommentsStore WHERE cid = %s", (k.get_cid()));
                break;
            except Exception as e:
                print("未知错误: ", e);
            
        for j, k in enumerate(data):
            try:
                cursor.execute("INSERT INTO ACcommentsStore(cid, name, content) VALUES(%s, %s, %s)", \
                                  (k.get_cid(), \
                                   k.get_name(), \
                                   k.get_content()));
            except Exception as e:
                print("未知错误: ", e);
        
        print("store done!");
        cursor.close();
        conn.commit();
        conn.close();
    
    def clear(self, cids):
        conn = pymysql.connect(host = self.__dbinfo.get_host(), \
                                    port = self.__dbinfo.get_port(), \
                                    user = self.__dbinfo.get_user(), \
                                    passwd = self.__dbinfo.get_pwd(), \
                                    db = self.__dbinfo.get_dbname(), \
                                    charset = self.__dbinfo.get_charset());
        cursor = conn.cursor();
        for j, k in enumerate(cids):
            try:
                cursor.execute("DELETE FROM ACcommentsStore WHERE cid = %s", (k));
            except Exception:
                print("未知错误");
        
        
        cursor.close();
        conn.commit();
        conn.close();