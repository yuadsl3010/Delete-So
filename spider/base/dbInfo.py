#!/usr/bin/python
#coding=utf8

class dbInfo(object):
    __dbname = "";
    __host = "";
    __port = 0;
    __user = "";
    __pwd = "";
    __charset = "";

    def get_dbname(self):
        return self.__dbname


    def get_host(self):
        return self.__host


    def get_port(self):
        return int(self.__port)


    def get_user(self):
        return self.__user


    def get_pwd(self):
        return self.__pwd
    
    
    def get_charset(self):
        return self.__charset


    def set_dbname(self, value):
        self.__dbname = value


    def set_host(self, value):
        self.__host = value


    def set_port(self, value):
        self.__port = value


    def set_user(self, value):
        self.__user = value


    def set_pwd(self, value):
        self.__pwd = value


    def set_charset(self, value):
        self.__charset = value