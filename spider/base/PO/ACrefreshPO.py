#coding=utf8

class ACrefreshPO(object):
    '''
ACRefresh表的数据实体
评论刷新表
|
---投稿编号（主键）
|
---生成时间
|
---当前状态
    '''
    
    def get_id(self):
        return self.__id


    def get_create_time(self):
        return self.__createTime


    def get_status(self):
        return self.__status

    def set_id(self, value):
        self.__id = value


    def set_create_time(self, value):
        self.__createTime = value


    def set_status(self, value):
        self.__status = value


    __id = "";
    __status = "";
    __createTime = "";
    