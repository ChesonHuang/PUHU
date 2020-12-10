import requests
import json
import unittest
import HtmlTestRunner
import os
import sys
from time import sleep,time


class Test_Api_1(unittest.TestCase):
	def __init__(self,method='runtest'):
		super(Test_Weather_1,self).__init__(method)
		self.base_url = "https://www.hko.gov.hk/json/"
		self.url = "https://www.hko.gov.hk/json/DYN_DAT_MINDS_FND.json?{param}"
		self.headers = {'Content-Type': 'application/json;charset=UTF-8'}
		self.d = u2.connect(devices[0])
		self.t = None
		

	# run before case execute
	def setUp(self):
		print('setUp')
		# start the app
		self.d.app_start('hko.MyObservatory_v1_0')
		self.t =Tool(self.d)
		self.t.screenshot('weather_setup')
	

	# run after case execute
	def tearDown(self):
		print('tearDown')
		self.d.press('home')
		self.t.screenshot('weather_teardown')

	def test_api_001(self):
		now_time = (str(time()).replace('.',''))[0:13]
		r_get = requests.get(self.url.format(param=now_time))
		to_dict=json.loads(r_get.text)

		# change param
		to_dict['DYN_DAT_MINDS_FND']['Day1MaxTemp'] = {'Value_Eng': '30', 'Val_Chi': '30', 'Val_Eng': '30', 'Value_Chi': '30'}

		to_json = json.dumps(to_dict)
		res_json = requests.post(self.base_url,data=to_json,headers=self.headers)

		# verify
		self.d(description="向上瀏覽").click()
		sleep(5)
		self.t.screenshot('weather_001')
		#self.d(scrollable=True).fling.vert.forward()
		self.d(scrollable=True).scroll.to(text="9-Day Forecast")
		sleep(5)
		self.d(resourceId="hko.MyObservatory_v1_0:id/text", text="9-Day Forecast").click()
		sleep(5)
		self.t.screenshot('weather_001')

		# verify temperature
		temperature = self.d(resourceId="hko.MyObservatory_v1_0:id/sevenday_forecast_temp").get_text()
		self.assertEqual(temperature,'19 - 30°C')
		print('temperature of tomorrow is 19 - 30°C, passed')

		# Extract the relative humidity (e,g, 60 - 85%) for the day after tomorrow
		print('today is',to_dict['DYN_DAT_MINDS_FND']['Day1ForecastDate']['Value_Eng'])
		
		minRH = to_dict['DYN_DAT_MINDS_FND']['Day3MinRH']['Value_Eng']
		maxRH = to_dict['DYN_DAT_MINDS_FND']['Day3MaxRH']['Value_Eng']

		print('the day after tomorrow is',to_dict['DYN_DAT_MINDS_FND']['Day3ForecastDate']['Value_Eng'],': humidity is',minRH,'-',maxRH,'%')


if __name__=='__main__':
	unittest.main()
	