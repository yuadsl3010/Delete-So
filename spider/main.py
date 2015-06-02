#!/usr/bin/python

import time
import ConfigParser
import logging
from base.Constants import *
from base.Ac_Data import *

logging.basicConfig(level=logging.WARNING,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='/var/log/acmore.log',
    filemode='a')
#from acfun.process import forceRefresh
'''
forceRefresh_thread = forceRefresh()
forceRefresh_thread.start()
'''

def day_bak(bak, day):
	if day != time.localtime(time.time()).tm_mday\
	and time.localtime(time.time()).tm_hour == 4:
		logging.warn('start daily save...')
		bak.save()
		logging.warn('daily save done')
		return time.localtime(time.time()).tm_mday
	else:
		return day
	

def control():
	f = open(CONTROL, 'r+')
	c = f.readline()
	res = 0
	if c == '':
		res = 0
	elif int(c) == -1:
		res = -1
	else:
		res = 0
		
	return res 

day = time.localtime(time.time()).tm_mday
ac_comments = Ac_Data(1000000)
logging.warn('start loading...')
ac_comments.load()
logging.warn('loading done')
	
while True:
	time.sleep(3)
	config = ConfigParser.ConfigParser()
	config.read(CONFIG)
	num = int(config.get(CONFIG_PROC, PROC_NUM))
	for i in range(num):
		name = config.get(CONFIG_PROC, CONFIG_PROC + str(i))
		module = __import__(name + "." + MODULE_AFTER, fromlist=[MODULE_AFTER])
		
		process = getattr(module, PROC_CLASS_NAME)
		func = process()
		if control() == -1:
			logging.warn('start exit save...')
			ac_comments.save()
			logging.warn('exit save done')
			exit()
			
		day = day_bak(ac_comments, day)
		func.work(ac_comments)


