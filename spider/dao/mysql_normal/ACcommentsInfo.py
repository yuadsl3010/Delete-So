#coding=utf8

from pymysql.err import *
import pymysql

class ACcommentsInfo(object):
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
        for j, k in enumerate(data):
            try:
                cursor.execute("INSERT INTO ACcommentsInfo(id, type, title, up, postTime, url) VALUES(%s, %s, %s, %s, %s, %s)", \
                                  (k.get_id(), \
                                   k.get_type(), \
                                   k.get_title(), \
                                   k.get_up(), \
                                   k.get_post_time(), \
                                   k.get_url()));
            except IntegrityError:
                print("主键重复");
            except Exception as e:
                print("未知错误: ", e);
        
        cursor.close();
        conn.commit();
        conn.close();
        