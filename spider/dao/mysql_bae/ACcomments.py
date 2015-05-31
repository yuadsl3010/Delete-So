#!/usr/bin/python
#coding=utf8

import MySQLdb
import sys

class ACcomments(object):
    '''
评论搜集表各项操作
    '''
    __dbinfo = "";
    __conn = None
    __cursor = None
        
    def __init__(self, dbinfo):
        self.__dbinfo = dbinfo;
        
    def insert(self, data):
        if data == -1:
            return
        
        try:
            conn = MySQLdb.connect(host = self.__dbinfo.get_host(), \
                        port = self.__dbinfo.get_port(), \
                        user = self.__dbinfo.get_user(), \
                        passwd = self.__dbinfo.get_pwd(), \
                        db = self.__dbinfo.get_dbname(), \
                        charset = self.__dbinfo.get_charset())
            cursor = conn.cursor()
            if data.get_delete() == 1:
                try:
                    cursor.execute("INSERT INTO accomments_delete(cid, content, userName, layer, acid, isDelete, siji, checkTime)\
                                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", \
                                  (data.get_cid(), \
                                   data.get_content(), \
                                   data.get_user_name(), \
                                   data.get_layer(), \
                                   data.get_acid(), \
                                   data.get_delete(), \
                                   data.get_siji(), \
                                   data.get_check_time()))
                except Exception:
                    pass
                
            if data.get_siji() == 1:
                try:
                    cursor.execute("INSERT INTO accomments_siji(cid, content, userName, layer, acid, isDelete, siji, checkTime)\
                                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", \
                                  (data.get_cid(), \
                                   data.get_content(), \
                                   data.get_user_name(), \
                                   data.get_layer(), \
                                   data.get_acid(), \
                                   data.get_delete(), \
                                   data.get_siji(), \
                                   data.get_check_time()))
                except Exception:
                    pass
            
            cursor.close()
            conn.commit()
            conn.close()
              
        except Exception:
            pass
            
        return 0
        
    def save(self, data):
        if data == -1:
            return
        
        try:
            conn = MySQLdb.connect(host = self.__dbinfo.get_host(), \
                        port = self.__dbinfo.get_port(), \
                        user = self.__dbinfo.get_user(), \
                        passwd = self.__dbinfo.get_pwd(), \
                        db = self.__dbinfo.get_dbname(), \
                        charset = self.__dbinfo.get_charset())
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO accomments(cid, content, userName, layer, acid, isDelete, siji, checkTime)\
                                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", \
                              (data.get_cid(), \
                               data.get_content(), \
                               data.get_user_name(), \
                               data.get_layer(), \
                               data.get_acid(), \
                               data.get_delete(), \
                               data.get_siji(), \
                               data.get_check_time()))
            except Exception as e:
                print e
                pass
            
            cursor.close()
            conn.commit()
            conn.close()
              
        except Exception as e:
            print e
            pass
            
        return 0
    
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
            try:
                cursor.execute("DELETE FROM accomments");
            except Exception as e:
                print ("未知错误：", e)
                pass
                
            cursor.close();
            deleteSor.close();
            conn.commit();
            conn.close();
        except Exception:
            pass
        
        return
    
    def load(self):
        result = []
        page = 0
        try:
            conn = MySQLdb.connect(host = self.__dbinfo.get_host(), \
                                    port = self.__dbinfo.get_port(), \
                                    user = self.__dbinfo.get_user(), \
                                    passwd = self.__dbinfo.get_pwd(), \
                                    db = self.__dbinfo.get_dbname(), \
                                    charset = self.__dbinfo.get_charset());
            cursor = conn.cursor();
            while page < 1000:
                try:
                    cursor.execute("SELECT * FROM accomments LIMIT %s, 1000", page * 1000)
                    result += cursor.fetchall()
                except Exception as e:
                    print "未知错误：" + str(e)
                    pass
                finally:
                    page += 1
                
            cursor.close();
            conn.commit();
            conn.close();
        except Exception as e:
            pass
        
        return result
    