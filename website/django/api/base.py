#encoding: utf-8
'''
Created on 2015-05-10 16:11

author: Yu Zhenchuan
email: yuzhenchuan@delete.so
'''
import time
import os
from api.comments import *

black_list = 'D:/Documents/workspace/delete_so/templates/word_wall.txt'
def clear_word(content):
    init_root(black_list)
    if is_contain(content):
        return ''
    
    return content

def add_word(content):
    open(black_list, 'a').write(content + '\n')

def deny_address(ip_address):
    if ip_address == '127.0.0.1': #报文里面没有找到，暂时放他一马
        pass
    else:
        pass #todo: 惩罚操作
        