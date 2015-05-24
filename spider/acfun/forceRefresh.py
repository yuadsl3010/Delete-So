#!/usr/bin/python
#coding=utf8

from dao.daoFactory import *
from base.PO.ACrefreshPO import *
import threading
import time
import copy
import logging

#两个线程都要修改临界资源buf，所以需要上锁
refresh_mutex = threading.Lock()
refresh_buf = []

class forceRefresh(threading.Thread):
    ACRefresh = ""
    logging.basicConfig(level=logging.WARNING,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='/var/log/acmore.log',
        filemode='a');
        
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        while True:
            try:
                self.daoAC = daoFactory().getACdao();
                self.ACRefresh = self.daoAC.getACRefresh();
                self.ACcommentsStatus = self.daoAC.getACCommentsStatus();
                need_delete = []
                need_refresh = []
                try:
                    db_buf = self.get_buf_from_db()
                    self.process_refresh(db_buf, need_refresh, need_delete)
                    self.update_to_db(db_buf, need_delete)
                    self.ACcommentsStatus.log("acrefresh");
                except Exception as e:
                    print("DB error", e)
                    continue
                
                self.refresh(need_refresh)
                time.sleep(300);
            except Exception as e:
                print("error", e)
                continue
    
    def get_buf_from_db(self):
        rows = self.ACRefresh.get()
        res = []
        for row in rows:
            po = ACrefreshPO()
            po.set_id(int(row[0]))
            po.set_status(int(row[2]))
            res.append(po)
        return res
    
    def update_to_db(self, db_buf, need_delete):
        self.ACRefresh.update(db_buf)
        self.ACRefresh.delete(need_delete) 
    
    def refresh(self, tmpBuf):
        global refresh_buf
        
        #print("refresh_buf", refresh_buf)
        
        if refresh_mutex.acquire(1):
            refresh_buf = list(set(tmpBuf))
            refresh_mutex.release()
        #buf = buf.extend(tmpBuf)
    
    def Get_Global_Buf(self):
        return copy.copy(refresh_buf)
    
    def clear_refresh_data(self, buf):
        if refresh_mutex.acquire(1):
            for item in buf:
                try:
                    refresh_buf.remove(item)
                except Exception as e:
                    print(e)
            refresh_mutex.release()
            
    def process_refresh(self, db_buf, need_refresh, need_delete):
        space = 100 - len(refresh_buf)
        for item in db_buf:
            if space > 0:
                status = int(item.get_status())
                #5分钟刷新一次，所以这里的逻辑是分别是0、1、3、6小时刷新
                if status == 0 or status == 12 or status == 36 or status == 72:
                    need_refresh.append(str(item.get_id()))
                    status = status + 1
                    item.set_status(status)
                    space = space - 1
                elif status > 72:
                    need_delete.append(str(item.get_id()))
                else :
                    status = status + 1
                    item.set_status(status)
            else :
                break
                    
