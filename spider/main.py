#!/usr/bin/python

import time
import sys
import ConfigParser
import thread
from base.Constants import *
#from acfun.process import forceRefresh
'''
forceRefresh_thread = forceRefresh()
forceRefresh_thread.start()
'''

while True:
	time.sleep(3);
	config = ConfigParser.ConfigParser();
	config.read(CONFIG);
	num = int(config.get(CONFIG_PROC, PROC_NUM));
	for i in range(num):
		name = config.get(CONFIG_PROC, CONFIG_PROC + str(i));
		module = __import__(name + "." + MODULE_AFTER, fromlist=[MODULE_AFTER]);
		process = getattr(module, PROC_CLASS_NAME);
		func = process();
		func.work();