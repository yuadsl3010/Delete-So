'''
Created by auto_sdk on 2015.04.22
'''
from top.api.base import RestApi


class TopTestDelayRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.sleep_time = None

	def getapiname(self):
		return 'taobao.top.test.delay'
