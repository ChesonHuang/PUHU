import os
# -*- coding: utf-8 -*-
import uiautomator2 as u2


class Tool():
	def __init__(self,device):
		self.u = device
		self.p = os.path.join(os.path.dirname(os.path.abspath(__file__)),'screenshot')

	def screenshot(self,name):
		if not os.path.exists(self.p):
			os.makedirs(self.p)

		pic = os.path.join(self.p,name+'.jpg')
		self.u.screenshot(pic)
		print('screenshot:'+pic)