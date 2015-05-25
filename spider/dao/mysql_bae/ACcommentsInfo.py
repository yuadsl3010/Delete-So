#!/usr/bin/python
#coding=utf8

import MySQLdb

class ACcommentsInfo(object):
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
                    cursor.execute("INSERT INTO accommentsinfo(id, type, title, up, postTime, url) VALUES(%s, %s, %s, %s, %s, %s)", \
                                      (k.get_id(), \
                                       k.get_type(), \
                                       k.get_title(), \
                                       k.get_up(), \
                                       k.get_post_time(), \
                                       str(k.get_url())));
                except Exception as e:
                    pass
            
            cursor.close();
            conn.commit();
            conn.close();
        except Exception as e:
            pass;
        