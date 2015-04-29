#!/usr/bin/python
#coding=utf8

from base.Process import Process
from base.URL import urlWork
from base.Constants import *
from dao.daoFactory import *
from base.PO.ACcommentsInfoPO import *
from base.PO.ACcommentsPO import *
from base.PO.ACcommentsStorePO import *
from forceRefresh import *
import os
import time
import json
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import socket
import urllib
import urllib2
import logging

class process(Process, urlWork):
    '''
ACFUN的入口函数在这里。
    '''
    workTimeA = 0;
    workTimeB = 0;
    ACCommentsInfo = "";
    ACComments = "";
    ACCommentsStore = "";
    daoAC = "";
    refresh_data = []
    logging.basicConfig(level=logging.WARNING,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='/var/log/acmore.log',
        filemode='a');
        
    def work(self):
        workTimeA = time.time(); #性能统计
        self.initDB();
        refresh_data = forceRefresh().Get_Global_Buf()
        #urlContentTimeA = time.time(); #性能统计
        if len(refresh_data) < 20:
            front_urlData = self.get_refresh_data(refresh_data)
            urlContent = self.sendGet(ACFUN);
            logging.debug("parsing...");
            #urlContentTimeB = time.time(); #性能统计
            #print("获取首页源代码用时：" + str(urlContentTimeB - urlContentTimeA));
            if not self.checkURL(urlContent):
                logging.error("connect acfun fail.");
                return;
            
            urlData = self.parse(front_urlData, urlContent);
            logging.debug("analysing...");
        else :
            urlData = self.get_refresh_data(refresh_data)
            
        self.analyse(refresh_data, urlData);
        forceRefresh().clear_refresh_data(refresh_data)
        self.clearDB();
        workTimeB = time.time(); #性能统计
        logging.debug("acfun process call done, cost time : " + str(workTimeB - workTimeA) + "\n");
    '''
          数据结构约定：
          rows[row[投稿URL, 投稿类型, 投稿标题, UP主, 投稿时间], row, row...]
    '''
    def parse(self, front_urlData, src):
        max = 0; #max这个字段用来查询更多的投稿
        now = 0;
        rows = front_urlData;
        while True:
            cursor = 0; #保存字符串出现的位置
            row = ACcommentsInfoPO(); #保存一篇投稿抓取的内容
            
            #判断是否包含投稿链接
            cursor = src.find('<a href="');
            if cursor == -1:
                break;
            
            #抓取投稿类型
            src = src[cursor+9:];
            if src[0:5] == "/v/ac":
                row.set_type("视频");
            elif src[0:5] == "/a/ac":
                row.set_type("文章");
            else:
                continue;
            
            #判断是否为包含URL地址
            cursor = src.find('"');
            if cursor == -1:
                continue;
            
            #查询更多的投稿
            now = int(src[src.find("/ac")+3:cursor]);
            if max < now:
                max = now;
                
            #抓取投稿URL
            row.set_id(src[src.find("/ac")+3:cursor]);
            row.set_url(ACFUN + src[:cursor]);
            src = src[cursor+2:];
            
            #进入一些异常判断和投稿标题分析
            if not src[:23] == 'target="_blank" title="':
                continue;
            
            src = src[27:];
            cursor = src.find("&#13;");
            if cursor == -1 \
            or cursor > 150:
                continue;
            
            #抓取投稿标题
            row.set_title(src[:cursor]);
            src = src[cursor+10:];
            
            #判断是否为包含UP信息
            cursor = src.find("&#13;");
            if cursor == -1:
                continue;
            
            #抓取UP信息
            row.set_up(src[:cursor]);
            src = src[cursor+9:];
            
            #判断是否为包含投稿时间
            cursor = src.find(" / ");
            if cursor == -1:
                continue;
            
            #抓取投稿时间
            row.set_post_time(src[:cursor]);
            src = src[cursor+12:];
            
            #将row保存到rows中
            rows.append(row);
            
        self.create_more(rows, max);
        self.ACCommentsInfo.insert(rows);
        #parseTimeB = time.time(); #性能统计
        #print("parse用时:" + str(parseTimeB - parseTimeA));
        return rows;
    '''
          数据结构约定：
          rows[row[评论cid, 评论内容, 评论人用户名, 引用评论cid, 该评论楼层数, 投稿URL, 删除标志, 司机标志, 时间戳], row, row...]
    '''
    def analyse(self, refresh_data, src):
        #初始化一个row，不然极端情况下程序会崩溃
        row = [];
        for j, k in enumerate(src):
            strACid = str(k.get_url());
            row = []; #保存一篇投稿的评论
            acid = strACid[strACid.find("/ac")+3:];
            acid = self.clear_acid(acid)
            url = "http://www.acfun.tv/comment_list_json.aspx?contentId=" + acid + "&currentPage=1";
            #urlCommentTimeA = time.time(); #性能统计
            jsonContent = self.sendGet(url);
            flag = True;
            #urlCommentTimeB = time.time(); #性能统计
            #print("获取评论源代码用时：" + str(urlCommentTimeB - urlCommentTimeA));
            if not self.checkURL(jsonContent):
                logging.warning("connect acfun comments fail");
                try:
                    refresh_data.remove(acid)
                except:
                    continue;
                continue;
            
            try:
                j_obj = json.loads(jsonContent);
            except Exception as e:
                logging.warning("get acfun comments fail");
                try:
                    refresh_data.remove(acid)
                except:
                    continue;
                continue;
            
			#偶尔会出现找不到commentContentArr的情况
            try:
                #开始解析json评论
                for m, n in enumerate(j_obj["commentContentArr"]):
                    comment = ACcommentsPO(); #保存一条评论的内容
                    
                    comment.set_acid(int(acid)); #抓取投稿编号            
                    comment.set_cid(int(j_obj["commentContentArr"][n]["cid"])); #抓取评论cid
                    comment.set_content(j_obj["commentContentArr"][n]["content"]); #抓取评论内容
                    comment.set_user_name(j_obj["commentContentArr"][n]["userName"]); #抓取评论人用户名
                    comment.set_quote_cid(int(j_obj["commentContentArr"][n]["quoteId"])); #抓取引用评论cid
                    comment.set_layer(int(j_obj["commentContentArr"][n]["count"])); #抓取该评论楼层数
                    userID = int(j_obj["commentContentArr"][n]["userID"]); #抓取评论人用户ID
                    
                    #热评高度，先置为0
                    comment.set_height(0);
                    
                    #司机判断
                    self.checkSIJI(comment);
                    
                    #删除判断
                    self.checkDelete(comment, userID);
                    
                    #嘴炮标志，先写死
                    comment.set_zuipao(0);
                    
                    #时间戳
                    comment.set_check_time(str(datetime.datetime.now()));
                    
                    #数据下盘时间需要商量一下
                    row.append(comment);
                    
                    #不能浪费太多时间在拥有超大评论量的投稿上
                    if m > 3000:
                        flag = False;
                        logging.error("over 3000, drop it.");
                        break;
                    
            except Exception as e:
                logging.error("commentContentArr is not exist");
                try:
                    refresh_data.remove(acid)
                except:
                    continue;
                continue;
                
            #analyseJsonB = time.time(); #性能统计
            #print("解析评论json用时：" + str(analyseJsonB - analyseJsonA));
            
            #评论超过3K条时不参与分析
            #热门评论已经不准备抓取了
            if False:
                storeData = self.checkBest(row);
                for j, k in enumerate(storeData):
                    if k[0] > 10 and k[0] < 30:
                        tmp = [];
                        for i in range(0, k[0]):
                            po = ACcommentsStorePO();
                            po.set_cid(k[1]);
                            po.set_name(k[k[0] - i + 1].get_name());
                            po.set_content(k[k[0] - i + 1].get_content());
                            tmp.append(po);
                        
                        for m, n in enumerate(row):
                            if int(n.get_cid()) == int(k[1]):
                                row[m].set_height(k[0]);
                        
                        self.ACCommentsStore.insert(tmp);
                
            self.ACComments.insert(row);
                
        #analyseTimeB = time.time(); #性能统计
        #print("analyse用时:" + str(analyseTimeB - analyseTimeA));
        return row;
    
    def checkURL(self, urlContent):
        if urlContent == URL_EXCEPTION \
        or urlContent == URL_FUALT:
            return False;
        else:
            return True;
    #unfinished
    def checkSIJI(self, comment):
        if comment.get_content().find(u"佛曰：") > -1 \
        or comment.get_content().find(u"如是我闻：") > -1 \
        or comment.get_content().find(u"*：") > -1:
            comment.set_siji(1);
        elif comment.get_content().find(u"ed2k://") > -1:
            linkUrl = "ed2k:" + comment.get_content()[comment.get_content().find(u"ed2k://"):]
            encodedContent = comment.get_content().replace(self.encodeFoyu(linkUrl),linkUrl,1)
            comment.set_content(encodedContent)
            comment.set_siji(1)
        elif comment.get_content().find(u"magnet:?") > -1:
            linkUrl = "magnet:?" + comment.get_content()[comment.get_content().find(u"magnet:?"):]
            encodedContent = comment.get_content().replace(self.encodeFoyu(linkUrl),linkUrl,1)
            comment.set_content(encodedContent)
            comment.set_siji(1)
        else:
            comment.set_siji(0);
    
    #含有ed2k和磁力链的评论发送至与佛论禅转化成佛语
    def encodeFoyu(self, text):
        url = "http://www.keyfc.net/bbs/tools/tudou.aspx";
        values = {"orignalMsg": text,
                 "action": "Encode"};
        data = urllib.urlencode(values);
        request = urllib2.Request(url,data);
        try:
            response = urllib2.urlopen(request);
            responseText = response.read();
        #之前那种错误处理不行
        except Exception as e:
            logging.error("encode error:", e);
        encodedFoyu = responseText[responseText.find("佛曰") : responseText.find("]]></Message>")]
        response.close()
        return encodedFoyu
            
    def checkDelete(self, comment, userID):
        #判断是否为已删除，为4则表示删除
        if userID == 4:
            comment.set_delete(1);
        else:
            comment.set_delete(0);
    
    def checkBest(self, comment):
        rows = []; #保存一篇投稿的所有的热门评论
        for j, m in enumerate(comment):
            row = [0, 0]; #保存一篇投稿的一段热门评论
            next = m.get_quote_cid(); #quoteid
            flag = True;
            while next != 0:
                for k, n in enumerate(comment):
                    tmp = ACcommentsStorePO();
                    if n.get_cid() == next:
                        tmp.set_cid(n.get_cid());
                        tmp.set_name(n.get_user_name());
                        tmp.set_content(n.get_content());
                        row[0] = row[0] + 1;
                        row[1] = n.get_cid();
                        row.append(tmp);
                        next = n.get_quote_cid();
                        if next == 0:
                            break;
            
            for m, n in enumerate(rows):
                if n[1] == row[1]:
                    flag = False;
                    if n[0] < row[0]:
                        rows[m] = row;
                        
                    break;

            if flag:
                rows.append(row);
        
        return rows;
    
    def initDB(self):
        self.daoAC = daoFactory().getACdao();
        self.ACCommentsInfo = self.daoAC.getACCommentsInfo();
        self.ACComments = self.daoAC.getACComments();
        self.ACCommentsStore = self.daoAC.getACCommentsStore();
        self.ACcommentsStatus = self.daoAC.getACCommentsStatus();
        self.ACcommentsStatus.log("acfunstart");
        
    def clearDB(self):
        logging.debug("clear...");
        row = self.ACComments.clear();
        #self.ACCommentsStore.clear(row);
        self.ACcommentsStatus.log("acfunend");
        if os.path.getsize("/var/log/acmore.log") > 1048576:
            os.system("> /var/log/acmore.log");
            
    #用来构造更多投稿的字段
    def create_more(self, rows, id):
        for i in range(1, 50):
            row = ACcommentsInfoPO();
            now_id = str(id - i);
            row.set_id(now_id);
            row.set_url(ACFUN_URL + now_id);
            row.set_type("秘密");
            row.set_title("秘密");
            row.set_up("秘密");
            row.set_post_time("1992-06-17 01:02:03");
            rows.append(row);
    
    #用来构造别人搜索过的输入
    def get_refresh_data(self, buf):
        rows = []
        for item in buf:
            row = ACcommentsInfoPO()
            row.set_type("秘密")
            row.set_id(str(item))
            row.set_url(ACFUN_URL + str(item))
            row.set_title("秘密")
            row.set_up("秘密")
            row.set_post_time("1992-06-17 01:02:03")
            rows.append(row)
        
        self.ACCommentsInfo.insert(rows);
        return rows
            
    #抓取的ac编号很可能是ac123_2的形式，需要加以过滤，否则写数据库的时候程序会core掉
    def clear_acid(self, acid):
        i = acid.find("_")
        if i > 0:
            acid = acid[:i]
        
        return acid
            