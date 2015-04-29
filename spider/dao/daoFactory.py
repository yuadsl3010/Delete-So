#!/usr/bin/python
#coding=utf8

import ConfigParser
from base.Constants import *
from dao.mysql_bae.ACdaoMysqlBae import *;
from base.dbInfo import *;

class daoFactory(object):
    '''
    type:
    1--- mysql, bae
    2--- mysql, normal
    '''
    __type = 0;
    __dbInfo = dbInfo();
    
    def __init__(self):
        config = ConfigParser.ConfigParser();
        config.read(CONFIG);
        self.__type = int(config.get(CONFIG_DB, DB_TYPE));
        self.__dbInfo.set_dbname(config.get(CONFIG_DB, DB_NAME));
        self.__dbInfo.set_host(config.get(CONFIG_DB, DB_HOST));
        self.__dbInfo.set_port(config.get(CONFIG_DB, DB_PORT));
        self.__dbInfo.set_user(config.get(CONFIG_DB, DB_USER));
        self.__dbInfo.set_pwd(config.get(CONFIG_DB, DB_PWD));
        self.__dbInfo.set_charset(config.get(CONFIG_DB, DB_CHARSET));
        
    def getACdao(self):
        if self.__type == 1:
            return ACdaoMysqlBae(self.__dbInfo);
        elif self.__type == 2:
            return 0;#ACdaoMysqlNormal(self.__dbInfo);
        else:
            print("DB type error, check the configure.");