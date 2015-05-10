#encoding: utf-8
'''
Created on 2015-05-10 04:31

author: Yu Zhenchuan
email: yuzhenchuan@delete.so
'''

#主要用以操作 被删除的评论
from django.http import JsonResponse

def get_delete_content(request):
    a = range(100)
    return JsonResponse(a, safe=False)