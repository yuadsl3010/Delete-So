#encoding: utf-8
'''
Created on 2015-05-10 04:37

author: Yu Zhenchuan
email: yuzhenchuan@delete.so
'''

import time
import os
from django.utils import timezone

class Node(object):  
    def __init__(self):  
        self.children = None  

root_nodes = Node()  
time_now = time.mktime(
                time.strptime(
                    timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
                    '%Y-%m-%d %H:%M:%S'
                    )
                )
# The encode of word is UTF-8  
def add_word(root, word):  
    node = root_nodes  
    for i in range(len(word)):  
        if node.children == None:  
            node.children = {}  
            node.children[word[i]] = Node()  
  
        elif word[i] not in node.children:  
            node.children[word[i]] = Node()  
  
        node = node.children[word[i]]  
  
def init_root(path): 
    global time_now 
    global root_nodes
    time_file = time.mktime(
                    time.strptime(
                        time.ctime(os.path.getmtime(path))
                        )
                    )
    if time_now == time_file:
        return root_nodes
    else:
        time_now = time_file
        
    root_nodes = Node()
    fp = open(path,'r')  
    for line in fp:  
        line = line[0:-1]  
        #print len(line)  
        #print line  
        #print type(line)  
        add_word(root_nodes, line)  
    fp.close()  
    return root_nodes  
  
# The encode of word is UTF-8  
# The encode of message is UTF-8  
def is_contain(message):  
    for i in range(len(message)):  
        p = root_nodes  
        j = i  
        while (j < len(message) and p.children != None and message[j] in p.children):  
            p = p.children[message[j]]  
            j = j + 1  
  
        if p.children == None:  
            #print '---word---',message[i:j]  
            return True  
      
    return False  