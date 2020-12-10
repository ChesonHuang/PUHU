import unittest
import HtmlTestRunner
import os
import sys
from time import sleep

cur_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cur_path,'..'))
from tool import *
from env_install import devices

class Test_Weather_1(unittest.TestCase):
	def __init__(self,method='runtest'):
		super(Test_Weather_1,self).__init__(method)
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


	def test_tomorrow_weather_001(self):
		#today =
		self.d(description="向上瀏覽").click()
		sleep(5)
		self.t.screenshot('weather_001')
		#self.d(scrollable=True).fling.vert.forward()
		self.d(scrollable=True).scroll.to(text="9-Day Forecast")
		sleep(5)
		self.d(resourceId="hko.MyObservatory_v1_0:id/text", text="9-Day Forecast").click()
		sleep(5)
		self.t.screenshot('weather_001')
		
		# verify day
		tomorrow = self.d(resourceId="hko.MyObservatory_v1_0:id/sevenday_forecast_date").get_text()
		self.assertEqual(tomorrow,'11 Dec')
		print('date of tomorrow is 11 Dec, passed')
		
		week = self.d(resourceId="hko.MyObservatory_v1_0:id/sevenday_forecast_day_of_week").get_text()
		self.assertEqual(week,'(Fri)')
		print('week of tomorrow is (Fri), passed')

		# verify temperature
		temperature = self.d(resourceId="hko.MyObservatory_v1_0:id/sevenday_forecast_temp").get_text()
		self.assertEqual(temperature,'19 - 24°C')
		print('temperature of tomorrow is 19 - 24°C, passed')

		# verify humidity
		humidity = self.d(resourceId="hko.MyObservatory_v1_0:id/sevenday_forecast_rh").get_text()
		self.assertEqual(humidity,'65 - 90%')
		print('humidity of tomorrow is 65 - 90%, passed')

		# verify force
		force = self.d(resourceId="hko.MyObservatory_v1_0:id/sevenday_forecast_wind").get_text()
		self.assertEqual(force,'Northeast force 3 to 4.')
		print('force of tomorrow is Northeast force 3 to 4., passed')

		# verify description
		description = self.d(resourceId="hko.MyObservatory_v1_0:id/sevenday_forecast_details").get_text()
		exp_desc ='One or two light rain patches in the morning and at night. Bright periods during the day.'
		self.assertEqual(description,exp_desc)
		print('description of tomorrow weather is',exp_desc,', passed')

		
if __name__=='__main__':
	unittest.main()