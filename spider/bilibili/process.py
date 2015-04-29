'''
Created on 2014年8月1日

@author: yzc
'''

from acmore.base.Process import Process
from acmore.base.URL import urlWork

class process(Process, urlWork):
    '''
ACFUN的入口函数在这里。
    '''

    def work(self):
        print("这里是bilibili的process函数"); 
        urlContent = self.sendGet(self, "http://www.acfun.tv");
        print("网页内容抓取:", urlContent[0:20]);
        pSrc = self.parse(self, urlContent[0:20]);
        aSrc = self.analyse(self, pSrc);
        print(aSrc);
        print("整个Process流程调用结束");   
             
    def parse(self, src):
        print("这里是bilibili的parse函数"); 
        print("传入的src =", src);
        return "parse之后的数据";
    
    def analyse(self, src):
        print("这里是bilibili的analyse函数"); 
        print("传入的src =", src);
        return "analyse之后的数据";