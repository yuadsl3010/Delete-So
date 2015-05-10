#encoding: utf-8
'''
Created on 2015-05-09 17:19

author: Yu Zhenchuan
email: yuzhenchuan@delete.so
'''

import time
from django.views.decorators.csrf import requires_csrf_token 
from django.shortcuts import render_to_response
from AliModel.models import db_commentdb, db_comment2db
from api.base import clear_word, deny_address
from django.forms.models import model_to_dict
from django.http import JsonResponse

def init_delete_so(request):
    return render_to_response('index.html', locals())

@requires_csrf_token #前端POST的时候需要校验csrf
def refresh_ds_comments(request):
    #输出数据
    json_result = dict()
    if request.method != 'POST':
        pass
    else:
        #获取用户输入数据
        username = request.POST.get('username', '')
        content = request.POST.get('content', '')
        position = request.POST.get('position', '')
        date = time.strftime("%Y-%m-%d %H:%M:%S")
        page = request.GET.get('page', '')
        
        #获取请求基础信息
        try:
            ip_address = request.META['REMOTE_ADDR']
        except Exception:
            ip_address = '127.0.0.1'
        
        
        #数据清理
        content = clear_word(content) #过滤敏感词、小广告等，一旦发现，立刻将content置空
        if len(page) == 0: #page为评论的页数
            page = 0
        else:
            page = int(page) 
            
        #录入数据的操作
        if len(content) == 0:
            deny_address(ip_address) #惩罚这个IP地址?
        else:
            if position == '0': #用户操作为新建一条留言
                new_comment = db_commentdb(userName=username,
                                           contents=content, 
                                           sortDate=date,
                                           postDate=date)
                new_comment.save() #直接插入数据到留言表即可
            else: #用户操作为评论别人的留言
                new_comment2 = db_comment2db(cid=position,
                                            userName=username,
                                            contents=content,
                                            postDate=date)
                new_comment2.save() #先插入数据到留言评论表
                
                db_commentdb.objects.filter(cid=position).update(sortDate=date) #再更新留言表的时间即可

            return JsonResponse(json_result)
            
        #回显数据的操作
        total_comments = int(db_commentdb.objects.all().count()) #获取共有多少留言，用以留言板的page显示
        qs_comments = db_commentdb.objects.all().order_by('-sortDate')[page*10:page*10+10] #只获取一个页面的留言内容
        result_comments = []
        for qs in qs_comments:
            dict_comments = model_to_dict(qs)
            comments2_cid = dict_comments['cid'] #将queryset转换为字典来组成json
            qs_comments2 = db_comment2db.objects.filter(cid=comments2_cid) #获取该留言下的评论
            dict_comments2 = []
            for qs_foo in qs_comments2: #将queryset转换为字典来组成json
                dict_comments2_foo = model_to_dict(qs_foo)
                dict_comments2.append(dict_comments2_foo)
                
            dict_comments['comment2'] = dict_comments2 #将留言下的评论放入该条留言中
            result_comments.append(dict_comments)
            
        #构造回显的json
        json_result['total'] = total_comments
        json_result['result'] = result_comments
        print JsonResponse(json_result)
        
    return JsonResponse(json_result)