#!/usr/bin/python
#coding=utf8

import HTMLParser
from base.URL import urlWork;
#import pymysql
class acfunHtmlHandler(HTMLParser):

    def __init__(self):
        self.contributionData = [None] * 7
        self.titleData = [None] * 5
    
    def index_2dFind(self, l, k):
        for i, j in enumerate(l):
            if k in j:
                return i
            
    def readComments(self,url):
        urlWork =  urlWork()
        if urlWork.sendGet(url) != "URL EXCEPTION" and urlWork.sendGet(url) != "STATUS FAULT":
            return urlWork.sendGet(url)
        return
    
    def resolveTitleData(self, title):
        #TBD:使用正则表达式
        i = title.find("标题: ")
        j = title.find("&#13")
        if (i != -1 and j != -1):
            return
        self.titleData[0] = title[i+4:j]#标题
        i = title.find("UP主: ")
        j = title.find("&#13", j+4)
        if (i != -1 and j != -1):
            return
        self.titleData[1] = title[i+5:j]#UP主
        i = title.find("发布于 ")
        j = title.find(" /")
        if (i != -1 and j != -1):
            return
        self.titleData[2] = title[i+4:j]#发布时间
        i = title.find("点击数: ")
        j = title.find(" /",j+2)
        if (i != -1 and j != -1):
            return
        self.titleData[3] = title[i+5:j]#点击数
        i = title.find("评论数: ")
        if (i != -1):
            return
        self.titleData[4] = title[i+5:]#评论数
        return self.titleData 
    
    #保留原本评论解析方法 ，弃用   
    """def getCommentPageList(self, commentText):                    
        totalPage = int(commentText[commentText.find("totalPage")+11:commentText.find(''',"pageSize":''')])
        commentIdList = []
        i = 1
        while(i<=totalPage):
            commentIdList.append(commentText[commentText.find('''"commentList":[''') + 
                        15 : commentText.find('''],"commentContentArr''')].split(","))
            i = i + 1"""
            
            
    def resolveCommentFile(self, commentText):
        #TBD：使用正则表达式
        i,j = 0
        commentList, quoteList = []
        while True:
            i = commentText.find('"cid":', j)
            j = i + 6 
            if i == -1:
                break
            cidString = commentText[j:commentText.find(',"content"', j)]
            commentList.append(int(cidString))
        
        #while True:
    
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            if "href" in attrs:
                i = self.index_2dFind(self, attrs, "href")
                if "/a/ac" in attrs[i][1]:
                    self.contributionData[0] = "文章"#投稿类型
                elif "/v/ac" in attrs[i][1]:
                    self.contributionData[0] = "视频"#投稿类型
                else:
                    return 
                j = self.index_2d(self, attrs, "title")
                if self.resolveTitleData(attrs[j][1])!= None:
                    t = self.resolveTitleData(attrs[j][1])
                    self.contributionData[1] = "www.acfun.tv" + attrs[i][1]#完整链接
                    self.contributionData[2] = t[0]#标题
                    self.contributionData[3] = t[1]#UP主
                    self.contributionData[4] = t[2]#发布时间
                    self.contributionData[5] = t[3]#点击数
                    self.contributionData[6] = t[4]#评论数
                if self.readComments(self.contributionData[1]) != None:
                    commentText = self.readComments("http://www.acfun.tv/comment_list_json.aspx?contentId=" + 
                                                 attrs[i][1][5:] + "&currentPage=1")
                












