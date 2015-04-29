#coding=utf8

class CommentsPO(object):
    '''
留言表 -- 可耻的照抄AC
|
---留言cid（主键，自增）
|
---留言内容
|
---引用留言quoteid
|
---自身楼数layer
|
---发送时间
    '''

    def get_id(self):
        return self.__id


    def get_content(self):
        return self.__content


    def get_quoteid(self):
        return self.__quoteid


    def get_layer(self):
        return self.__layer


    def get_time(self):
        return self.__time


    def set_id(self, value):
        self.__id = value


    def set_content(self, value):
        self.__content = value


    def set_quoteid(self, value):
        self.__quoteid = value


    def set_layer(self, value):
        self.__layer = value


    def set_time(self, value):
        self.__time = value

    
    __id = "";
    __content = "";
    __quoteid = "";
    __layer = "";
    __time = "";    
