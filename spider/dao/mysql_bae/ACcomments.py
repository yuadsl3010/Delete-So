#!/usr/bin/python
#coding=utf8

import MySQLdb
import sys

class ACcomments(object):
    '''
评论搜集表各项操作
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
                if k.get_delete() == 1:
                    cursor.execute("UPDATE accomments SET checkTime = %s, height = %s, siji = %s, zuipao = %s, isDelete = %s WHERE cid = %s", \
                                   (k.get_check_time(), \
                                    k.get_height(), \
                                    k.get_siji(), \
                                    k.get_zuipao(), \
                                    k.get_delete(), \
                                    k.get_cid()));
                else:
                    try:
                        cursor.execute("INSERT INTO accomments(cid, content, userName, quoteCid, layer, acid, height, isDelete, siji, zuipao, checkTime) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", \
                                              (k.get_cid(), \
                                               k.get_content(), \
                                               k.get_user_name(), \
                                               k.get_quote_cid(), \
                                               k.get_layer(), \
                                               k.get_acid(), \
                                               k.get_height(), \
                                               k.get_delete(), \
                                               k.get_siji(), \
                                               k.get_zuipao(), \
                                               k.get_check_time()));
                    except Exception as e:
                        cursor.execute("UPDATE accomments SET checkTime = %s, height = %s, siji = %s, zuipao = %s, isDelete = %s WHERE cid = %s", \
                                       (k.get_check_time(), \
                                        k.get_height(), \
                                        k.get_siji(), \
                                        k.get_zuipao(), \
                                        k.get_delete(), \
                                        k.get_cid()));
                        pass;#print("未知错误: ", e);
            
            cursor.close();
            conn.commit();
            conn.close();        
        except Exception as e:
            pass;
        
    def clear(self):
        try:
            conn = MySQLdb.connect(host = self.__dbinfo.get_host(), \
                                    port = self.__dbinfo.get_port(), \
                                    user = self.__dbinfo.get_user(), \
                                    passwd = self.__dbinfo.get_pwd(), \
                                    db = self.__dbinfo.get_dbname(), \
                                    charset = self.__dbinfo.get_charset());
            cursor = conn.cursor();
            deleteSor = conn.cursor();
            row = [];
            try:
                cursor.execute("SELECT cid FROM accomments WHERE height = 0 AND isDelete = 0 AND siji = 0 AND zuipao = 0 AND checkTime < DATE_SUB(NOW(), INTERVAL 3 DAY) LIMIT 1000");
                results = cursor.fetchall()
                for data in results:
                    deleteSor.execute("DELETE FROM accomments WHERE cid = %s LIMIT 1", (data));
                    deleteSor.execute("DELETE FROM accommentsstore WHERE cid = %s LIMIT 3000", (data));
            except Exception as e:
                print("未知错误：", e);
                
            cursor.close();
            deleteSor.close();
            conn.commit();
            conn.close();
        except Exception as e:
            return 0;
        return row;
    