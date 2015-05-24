#encoding: utf-8
'''
Created on 2015-05-09 17:19

author: Yu Zhenchuan
email: yuzhenchuan@delete.so
'''

from django.shortcuts import render_to_response

def init_delete_so(request):
    return render_to_response('index.html', '')

def do_search(request):    
    return render_to_response('search.html', '')
