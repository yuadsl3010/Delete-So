#coding=utf8

class ACcommentsStorePO(object):
    '''
ACcommentsStore表的数据实体
评论搜集表（底下的回复）--评论搜集表一条记录对应此表多条记录
|
---评论cid（不需要主键，可重复）
|
---评论人用户名（这地方可以挖掘个新功能，这条记录用户名很多重复出现的时候可以判定为热门讨论/嘴炮，体现在评论搜集表的嘴炮标志中）
|
---评论内容
    '''

    def get_cid(self):
        return self.__cid


    def get_name(self):
        return self.__name


    def get_content(self):
        return self.__content


    def set_cid(self, value):
        self.__cid = value


    def set_name(self, value):
        self.__name = value


    def set_content(self, value):
        self.__content = value


    __cid = "";
    __name = "";
    __content = "";
    