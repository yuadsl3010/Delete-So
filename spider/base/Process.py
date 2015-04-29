#!/usr/bin/python
#coding=utf8

import abc

class Process(object):
    __metaclass__ = abc.ABCMeta;
    '''
main函数里调用的是继承Process的类，由Process来调用Parse和Analyse。
这样做的好处是我们可以通过反射机制将多个Process写入配置文件中，方便以后Process的拓展。
此类继承了urlWork，可完成get和post请求的操作。
虽然目前只有ACMore一个Process。
    '''

    @abc.abstractmethod
    def work(self):
        '''
        Constructor
        '''
        return;
    
    @abc.abstractmethod
    def parse(self, src):
        '''
        用以<直接>获取并<初步分析>网页源代码的方法。
        这里我认为经过src应当为一条明确的地址，方便我们的抓取。
        '''
        return;  
    
    @abc.abstractmethod
    def analyse(self, src):
        '''
        用以从parse方法的结果中<分析>获取我们需要内容的方法。
        这里我认为经过parse的数据src应当是string类型的二维数组，方便一条一条进行分析。
        '''
        return;