'''
Created on 2015-05-09 10:13

author: Yu Zhenchuan
email: yuzhenchuan@delete.so
'''

from django.shortcuts import render_to_response
from AliModel.models import db_status

def testdb(request):
    status_list = db_status.objects.all()
    
    return render_to_response('status.html', locals())