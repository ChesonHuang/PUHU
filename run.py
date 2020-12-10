from HtmlTestRunner import HTMLTestRunner
import os
import unittest
import sys
from tool import *
import TestCases

cur_path = os.path.dirname(os.path.abspath(__file__))

def run(suites,reportname):
	report_path = os.path.join(cur_path,'Reports')
	if not os.path.exists(report_path):
		os.mkdirs(report_path)
	report_name = os.path.join(report_path,reportname+'.txt')
	with open(report_name,'w') as fp:
		runner = HTMLTestRunner(stream=fp,report_title='MyObservatory Testing Report',descriptions='Description')
		runner.run(suites)


def suite(name,tc_type='simple'):
	suites = None
	if tc_type == 'simple':
		suites = unittest.TestSuite()
		suites.addTest(name)
	else:
		test_dir = os.path.join(cur_path,'TestCases',name)
		suites = unittest.defaultTestLoader.discover(test_dir, pattern='test_*.py',top_level_dir=None)
	return suites

if __name__=='__main__':
	suites=suite('.',tc_type='multi')
	print(suites)
	run(suites,'test_weather_1')

