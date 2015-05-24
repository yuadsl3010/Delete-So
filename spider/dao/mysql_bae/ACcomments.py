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
        total_comm = 0
        try:
            conn = MySQLdb.connect(host = self.__dbinfo.get_host(), \
                        port = self.__dbinfo.get_port(), \
                        user = self.__dbinfo.get_user(), \
                        passwd = self.__dbinfo.get_pwd(), \
                        db = self.__dbinfo.get_dbname(), \
                        charset = self.__dbinfo.get_charset()); 
            cursor = conn.cursor();
            #这个地方传进来的是一个二维数组，类似：
            #[投稿1, 投稿2, 投稿3...]，而每一个投稿又是：
            #[评论1，评论2，评论3...]
            for comm in data:
                total_comm += 1
                if int(comm.get_siji()) == 1:
                    try:
                        cursor.execute("INSERT INTO accomments_siji(cid, content, userName, quoteCid, layer, acid, height, isDelete, siji, zuipao, checkTime) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", \
                                                  (comm.get_cid(), \
                                                   comm.get_content(), \
                                                   comm.get_user_name(), \
                                                   comm.get_quote_cid(), \
                                                   comm.get_layer(), \
                                                   comm.get_acid(), \
                                                   comm.get_height(), \
                                                   comm.get_delete(), \
                                                   comm.get_siji(), \
                                                   comm.get_zuipao(), \
                                                   comm.get_check_time()));
                    except Exception:
                        pass
                elif int(comm.get_delete()) == 1:
                    try:
                        cursor.execute("INSERT INTO accomments_delete SELECT * FROM accomments WHERE cid = %s", \
                                       comm.get_cid());
                    except Exception:
                        pass
                else:
                    try:
                        cursor.execute("INSERT INTO accomments(cid, content, userName, quoteCid, layer, acid, height, isDelete, siji, zuipao, checkTime) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", \
                                              (comm.get_cid(), \
                                               comm.get_content(), \
                                               comm.get_user_name(), \
                                               comm.get_quote_cid(), \
                                               comm.get_layer(), \
                                               comm.get_acid(), \
                                               comm.get_height(), \
                                               comm.get_delete(), \
                                               comm.get_siji(), \
                                               comm.get_zuipao(), \
                                               comm.get_check_time()));
                    except Exception:
                        cursor.execute("UPDATE accomments SET checkTime = %s, height = %s, siji = %s, zuipao = %s, isDelete = %s WHERE cid = %s", \
                                       (comm.get_check_time(), \
                                        comm.get_height(), \
                                        comm.get_siji(), \
                                        comm.get_zuipao(), \
                                        comm.get_delete(), \
                                        comm.get_cid()));
                        pass;#print("未知错误: ", e);
                
            cursor.close(); 
            conn.commit();
            conn.close();  
                                  
        except Exception:    
            return 0
        
        return total_comm
        
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
                cursor.execute("DELETE FROM accomments WHERE checkTime < DATE_SUB(NOW(), INTERVAL 3 DAY) LIMIT 1000");
            except Exception as e:
                #print ("未知错误：", e)
                pass
                
            cursor.close();
            deleteSor.close();
            conn.commit();
            conn.close();
        except Exception as e:
            pass
        
        return
    
    def open_conn(self):
        try:
            self.__conn = MySQLdb.connect(host = self.__dbinfo.get_host(), \
                        port = self.__dbinfo.get_port(), \
                        user = self.__dbinfo.get_user(), \
                        passwd = self.__dbinfo.get_pwd(), \
                        db = self.__dbinfo.get_dbname(), \
                        charset = self.__dbinfo.get_charset()); 
            self.__cursor = self.__conn.cursor();
        except Exception as e:
            print("open error：", e);
            return False
        
        return True
            
    def close_conn(self):
        try:
            self.__cursor.close(); 
            self.__conn.commit();
            self.__conn.close();   
        except Exception as e:
            print ("close error：", e)