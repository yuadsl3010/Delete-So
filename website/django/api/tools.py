#encoding: utf-8
'''
Created on 2015年5月26日

@author: chuan
'''

import time

class clocker(object):
    '''
    用来统计时间的小工具
    '''
    clocks = ''

    def __init__(self):
        '''
        Constructor
        '''
        self.clocks = dict()
    
    def start(self, name):
        if self.clocks.has_key(str(name)):
            print 'clocker duplicate'
        else:
            self.clocks[str(name)] = time.time()
    
    def end(self, name):
        if not self.clocks.has_key(str(name)):
            print 'no such clocker'
        else:
            cost = time.time() - self.clocks[str(name)]
            self.clocks.pop(str(name))
            print 'clocker: ' + str(name) + ' cost time: ' + str(cost) + 's'
            print ' '
            