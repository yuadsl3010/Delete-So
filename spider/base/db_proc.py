#encoding: utf-8
'''
Created on 2015-05-31 14:51

author: Yu Zhenchuan
email: yuzhenchuan@delete.so
'''
from dao.daoFactory import *
from base.PO.ACcommentsInfoPO import *
from base.PO.ACcommentsPO import *
from base.PO.ACcommentsStorePO import *

class db_proc():
    #初始化数据库
    def __init__(self):
        self.daoAC = daoFactory().getACdao()
        self.ACCommentsInfo = self.daoAC.getACCommentsInfo()
        self.ACComments = self.daoAC.getACComments()
        self.ACCommentsStore = self.daoAC.getACCommentsStore()
        self.ACcommentsStatus = self.daoAC.getACCommentsStatus()