#encoding: utf-8
'''
Created on 2015-05-18 21:53

author: Yu Zhenchuan
email: yuzhenchuan@delete.so
'''

from api.base import *
from django.shortcuts import render_to_response

def add_black(request):
    request.encoding = 'utf-8'
    #输出数据
    status = '不理解。。。'
    
    #获取用户输入数据
    words = request.GET.get('words', '').encode('utf-8')
    auth = request.GET.get('auth', '').encode('utf-8')
    
    #防止有人手贱乱加黑名单
    if auth != 'yzc':
        return render_to_response('black_list.html', {'status': status})
    
    #敏感词放入后台检测的时候如果找不到，那么才加入黑名单
    if len(clear_word(words)) != 0:
        add_word(words)
        status = '敏感词已经添加成功'
    else:
        status = '该敏感词已经收录过了哟'
        
    return render_to_response('black_list.html', {'status': status})
        