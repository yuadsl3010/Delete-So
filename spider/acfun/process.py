#!/usr/bin/python
#coding=utf8

from base.Process import Process
from base.URL import urlWork
from base.Constants import *
from dao.daoFactory import *
from base.PO.ACcommentsInfoPO import *
from base.PO.ACcommentsPO import *
from base.PO.ACcommentsStorePO import *
from multiprocessing.dummy import Pool as ThreadPool 
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
import re

class process(Process, urlWork):
    '''
ACFUN的入口函数在这里。
    '''
    workTimeA = 0
    workTimeB = 0
    ACCommentsInfo = ""
    ACComments = ""
    ACCommentsStore = ""
    daoAC = ""
    #refresh_data = []
    work_score = []
    logging.basicConfig(level=logging.WARNING,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='/var/log/acmore.log',
        filemode='a')
        
    def work(self):
        workTimeA = time.time() #性能统计
        
        #将启动时间写入数据库
        self.initDB()
        #refresh_data = forceRefresh().Get_Global_Buf()
        #urlContentTimeA = time.time() #性能统计
        '''
        if len(refresh_data) < 20:
            front_urlData = self.get_refresh_data(refresh_data)
            urlContent = self.sendGet(ACFUN)
            logging.debug("parsing...")
            #urlContentTimeB = time.time() #性能统计
            #print("获取首页源代码用时：" + str(urlContentTimeB - urlContentTimeA))
            if not self.checkURL(urlContent):
                logging.error("connect acfun fail.")
                return
            
            urlData = self.parse(front_urlData, urlContent)
            logging.debug("analysing...")
        else :
            urlData = self.get_refresh_data(refresh_data)'''
            
        #self.analyse(refresh_data, urlData)
        #forceRefresh().clear_refresh_data(refresh_data)、
        
        #从acfun首页获取源代码用于解析热门投稿
        url_data = self.sendGet(ACFUN)
        
        #从HTML中得到我们所需要的数据，格式为[[u'/v/ac1873087', u'title="\u5168\u660e\u661f\u70ed\u5531happy"']...]
        parse_data = self.get_parse_data(url_data)
        
        #从每篇投稿中获取基本的信息
        analyse_data = self.parse(parse_data)
        
        #使用map进行多线程分析每篇投稿的评论
        pool = ThreadPool(16) 
        insert_data = pool.map(self.analyse, analyse_data) #这里的输出为ACComments结构体的数组
        pool.close()
        pool.join()
        
        #使用map进行多线程发送评论
        pool = ThreadPool(16) 
        self.work_score = pool.map(self.ACComments.insert, tuple(insert_data))
        pool.close()
        pool.join()
            
        #数据清理
        self.clearDB()
        workTimeB = time.time() #性能统计
        self.speed_cal(workTimeB - workTimeA)
        logging.debug("acfun process call done, cost time : " + str(workTimeB - workTimeA) + "\n")
        
    def get_parse_data(self, urlContent):
        parse_data = []
        
        pattern_1 = re.compile(r'''
            <a.*?</a>     
            ''', re.VERBOSE)
        pattern_2 = re.compile(r'''
            /a/ac[0-9]* | /v/ac[0-9]* | /v/ab[0-9]* |     #从<a xxxxx </a>中拿到投稿url和title就OK
            title=".*?"
            ''', re.VERBOSE)
        
        #按照<a xxxxx </a>解析
        src = pattern_1.findall(urlContent)
        
        #从<a xxxxx </a>中拿到投稿url和title就OK
        tmp = []
        for s in src:
            tmp = pattern_2.findall(s)
            if len(tmp) == 2:
                parse_data.append(tmp)
                
        return parse_data
        
    '''
          数据结构约定：
          rows[row[投稿URL, 投稿类型, 投稿标题, UP主, 投稿时间], row, row...]
    '''
    def parse(self, src):
        max = 0 #max这个字段用来查询更多的投稿
        now = 0
        rows = []#front_urlData
        for data in src:
            try:
                row = ACcommentsInfoPO() #保存一篇投稿抓取的内容
                
                #获取投稿类型
                if data[0][0:5] == '/v/ac':
                    row.set_id(data[0][5:])
                    row.set_type('视频')
                elif data[0][0:5] == '/a/ac':
                    row.set_id(data[0][5:])
                    row.set_type('文章')
                elif data[0][0:5] == '/v/ab':
                    #番剧的id和其他不一样，加负号以示区别
                    row.set_id('-' + data[0][5:])
                    row.set_type('番剧')
                else:
                    continue
                
                #获取acid和url
                row.set_url(ACFUN + data[0])
                
                #max这个字段用来查询更多的投稿，比如我从首页获取的最大投稿是ac190000，那么一会我会多抓去ac188900到ac190000的评论信息
                if max < int(data[0][5:]):
                    max = int(data[0][5:])
                    
                #到了解析title的时候了，A站的title写的很不规范，以下是我们需要分析的几种情况
                #情况1 什么都有，开工的时候要注意标题后面的两种冒号： title="标题: 抗战烽火孕育新中国国歌 《义勇军进行曲》唱响世界80年&#13;UP主: 亡是公&#13;发布于 2015-05-24 20:22:26 / 点击数: 2602 / 评论数: 96"
                #情况2 没有UP主，就一个更新时间，这种数据常见于番剧： title="标题：【四月】幻界战线 &#13;更新至：第8集 &#13;更新于：2015年05月24日"
                #情况3 这下更牛B，连更新时间都不需要了，一般是推荐 ： title="全明星热唱happy" 
                #情况4 还有这种有标题但没有UP主的                  ： title="标题: 我爱你 中国（A站爱国兔子合集）"
                
                #先过滤掉前面几个字
                data[1] = data[1][7:]
                
                #先排除情况3
                now = data[1].find('标题')
                if now == -1:
                    row.set_title(data[1][:len(data[1])-1].strip())
                    #然后开始疯狂捏造数据
                    row.set_up("UP主不详")
                    row.set_post_time("1992-06-17 01:02:03")
                else:
                    data[1] = data[1][3:]
                    #然后排除情况2
                    now = data[1].find('更新于')
                    if now != -1:
                        now = data[1].find('&#13;')
                        #获取title
                        row.set_title(data[1][:now].strip())
                        #然后也开始疯狂捏造数据
                        row.set_up("UP主不详")
                        row.set_post_time("1992-06-17 01:02:03")
                    else:
                        now = data[1].find('&#13;')
                        if now != -1:
                            #接着处理情况1
                            #获取title
                            row.set_title(data[1][:now].strip())
                            data[1] = data[1][now+1:]
                            
                            #获取UP主
                            now = data[1].find('&#13;')
                            row.set_up(data[1][9:now])
                            data[1] = data[1][now+1:]
                            
                            #获取投稿时间
                            now = data[1].find(' / ')
                            row.set_post_time(data[1][8:now])
                        else:
                            #最后是情况4
                            row.set_title(data[1][:len(data[1])-1].strip())
                            #然后开始疯狂捏造数据
                            row.set_up("UP主不详")
                            row.set_post_time("1992-06-17 01:02:03")
                    
            except Exception:
                continue
                
            rows.append(row)
        
        #开始随机抓取评论
        self.create_more(rows, max)
        #投稿信息单独放一张表
        self.ACCommentsInfo.insert(rows)
           
        return rows
    '''
          数据结构约定：
          rows[row[评论cid, 评论内容, 评论人用户名, 引用评论cid, 该评论楼层数, 投稿URL, 删除标志, 司机标志, 时间戳], row, row...]
    '''
    def analyse(self, src):
        #初始化一个row，不然极端情况下程序会崩溃
        row = [] #保存一篇投稿的评论
        strACid = int(src.get_id())
        acid = strACid
        #番剧的id小于0
        if acid > 0:
            url = "http://www.acfun.tv/comment_list_json.aspx?contentId=" + str(acid) + "&currentPage=1"
        else:
            url = 'http://www.acfun.tv/comment/bangumi/web/list?bangumiId=' + str(-acid) + '&pageNo=1'

        #urlCommentTimeA = time.time() #性能统计
        jsonContent = self.sendGet(url)
        flag = True
        #urlCommentTimeB = time.time() #性能统计
        #print("获取评论源代码用时：" + str(urlCommentTimeB - urlCommentTimeA))
        if not self.checkURL(jsonContent):
            logging.warning("connect acfun comments fail")
            '''
            try:
                refresh_data.remove(acid)
            except:
                continue
            '''    
            return 
        
        try:
            j_obj = json.loads(jsonContent)
        except Exception as e:
            logging.warning("get acfun comments fail")
            '''
            try:
                refresh_data.remove(acid)
            except:
                continue
            '''
            return 
        
        #番剧的id小于0
        try:
            if acid > 0:
                json_data = j_obj["commentContentArr"]
            else:
                json_data = j_obj['data']["commentContentArr"]
        except:
            logging.error("commentContentArr is not exist")
            return
        
		#偶尔会出现找不到commentContentArr的情况
        try:
            #开始解析json评论
            for m, n in enumerate(json_data):
                comment = ACcommentsPO() #保存一条评论的内容
                
                comment.set_acid(int(acid)) #抓取投稿编号            
                comment.set_cid(int(json_data[n]["cid"])) #抓取评论cid
                comment.set_content(json_data[n]["content"]) #抓取评论内容
                comment.set_user_name(json_data[n]["userName"]) #抓取评论人用户名
                comment.set_quote_cid(int(json_data[n]["quoteId"])) #抓取引用评论cid
                comment.set_layer(int(json_data[n]["count"])) #抓取该评论楼层数
                userID = int(json_data[n]["userID"]) #抓取评论人用户ID
                
                #热评高度，先置为0
                comment.set_height(0)
                
                #司机判断
                self.checkSIJI(comment)
                
                #删除判断
                self.checkDelete(comment, userID)
                
                #嘴炮标志，先写死
                comment.set_zuipao(0)
                
                #时间戳
                comment.set_check_time(str(datetime.datetime.now()))
                
                #数据下盘时间需要商量一下
                row.append(comment)
                
                #不能浪费太多时间在拥有超大评论量的投稿上
                if m > 3000:
                    flag = False
                    logging.error("over 3000, drop it.")
                    break
                
        except Exception as e:
            logging.error("commentContentArr is not exist")
            '''
            try:
                refresh_data.remove(acid)
            except:
                continue
            '''
            return 
            
        #analyseJsonB = time.time() #性能统计
        #print("解析评论json用时：" + str(analyseJsonB - analyseJsonA))
        
        #评论超过3K条时不参与分析
        #热门评论已经不准备抓取了
        '''
        if False:
            storeData = self.checkBest(row)
            for j, k in enumerate(storeData):
                if k[0] > 10 and k[0] < 30:
                    tmp = []
                    for i in range(0, k[0]):
                        po = ACcommentsStorePO()
                        po.set_cid(k[1])
                        po.set_name(k[k[0] - i + 1].get_name())
                        po.set_content(k[k[0] - i + 1].get_content())
                        tmp.append(po)
                    
                    for m, n in enumerate(row):
                        if int(n.get_cid()) == int(k[1]):
                            row[m].set_height(k[0])
                    
                    self.ACCommentsStore.insert(tmp)
        '''
        #self.ACComments.insert(row)
                
        #analyseTimeB = time.time() #性能统计
        #print("analyse用时:" + str(analyseTimeB - analyseTimeA))
        return row
    
    def checkURL(self, urlContent):
        if urlContent == URL_EXCEPTION \
        or urlContent == URL_FUALT:
            return False
        else:
            return True
    #unfinished
    def checkSIJI(self, comment):
        if comment.get_content().find(u"佛曰：") > -1 \
        or comment.get_content().find(u"如是我闻：") > -1 \
        or comment.get_content().find(u"*：") > -1:
            comment.set_siji(1)
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
            comment.set_siji(0)
    
    #含有ed2k和磁力链的评论发送至与佛论禅转化成佛语
    def encodeFoyu(self, text):
        url = "http://www.keyfc.net/bbs/tools/tudou.aspx"
        values = {"orignalMsg": text,
                 "action": "Encode"}
        data = urllib.urlencode(values)
        request = urllib2.Request(url,data)
        try:
            response = urllib2.urlopen(request)
            responseText = response.read()
        #之前那种错误处理不行
        except Exception as e:
            logging.error("encode error:", e)
        encodedFoyu = responseText[responseText.find("佛曰") : responseText.find("]]></Message>")]
        response.close()
        return encodedFoyu
            
    def checkDelete(self, comment, userID):
        #判断是否为已删除，为4则表示删除
        if userID == 4:
            comment.set_delete(1)
        else:
            comment.set_delete(0)
    
    def checkBest(self, comment):
        rows = [] #保存一篇投稿的所有的热门评论
        for j, m in enumerate(comment):
            row = [0, 0] #保存一篇投稿的一段热门评论
            next = m.get_quote_cid() #quoteid
            flag = True
            while next != 0:
                for k, n in enumerate(comment):
                    tmp = ACcommentsStorePO()
                    if n.get_cid() == next:
                        tmp.set_cid(n.get_cid())
                        tmp.set_name(n.get_user_name())
                        tmp.set_content(n.get_content())
                        row[0] = row[0] + 1
                        row[1] = n.get_cid()
                        row.append(tmp)
                        next = n.get_quote_cid()
                        if next == 0:
                            break
            
            for m, n in enumerate(rows):
                if n[1] == row[1]:
                    flag = False
                    if n[0] < row[0]:
                        rows[m] = row
                        
                    break

            if flag:
                rows.append(row)
        
        return rows
    
    def initDB(self):
        self.daoAC = daoFactory().getACdao()
        self.ACCommentsInfo = self.daoAC.getACCommentsInfo()
        self.ACComments = self.daoAC.getACComments()
        self.ACCommentsStore = self.daoAC.getACCommentsStore()
        self.ACcommentsStatus = self.daoAC.getACCommentsStatus()
        self.ACcommentsStatus.log("acfunstart")
        
    def clearDB(self):
        logging.debug("clear...")
        self.ACComments.clear()
        #self.ACCommentsStore.clear(row)
        self.ACcommentsStatus.log("acfunend")
        if os.path.getsize("/var/log/acmore.log") > 1048576:
            os.system("> /var/log/acmore.log")
            
    def speed_cal(self, time_val):
        logging.debug('speed cal...')
        scores = 0
        for score in self.work_score:
            scores += int(score)
            
        speed_val = int(scores / time_val)
        self.ACcommentsStatus.score(speed_val)
        
    #用来构造更多投稿的字段
    def create_more(self, rows, id):
        for i in range(1, 50):
            row = ACcommentsInfoPO()
            now_id = str(id - i)
            row.set_id(now_id)
            row.set_url(ACFUN_URL + now_id)
            row.set_type("类型未知")
            row.set_title("标题不详")
            row.set_up("UP主不详")
            row.set_post_time("1992-06-17 01:02:03")
            rows.append(row)
    
    #用来构造别人搜索过的输入
    def get_refresh_data(self, buf):
        rows = []
        for item in buf:
            row = ACcommentsInfoPO()
            row.set_type("类型未知")
            row.set_id(str(item))
            row.set_url(ACFUN_URL + str(item))
            row.set_title("标题不详")
            row.set_up("UP主不详")
            row.set_post_time("1992-06-17 01:02:03")
            rows.append(row)
        
        self.ACCommentsInfo.insert(rows)
        return rows
            
    #抓取的ac编号很可能是ac123_2的形式，需要加以过滤，否则写数据库的时候程序会core掉
    def clear_acid(self, acid):
        i = acid.find("_")
        if i > 0:
            acid = acid[:i]
        
        return acid
            