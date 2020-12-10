A simple Demo for automate the MyObservatory app on Andriod platform,which base on python+unittest+HTMLTestRunner+Uiautomator2, named PUHU.

Why adopt PUHU
	Compare to java, python is easier to develop and run our test cases. Consider to test app, Uiautomator2 is well known and it is suitable to operate. Moreover
	it support python. python has serveral test frame, such as pytest or unittest, either of them meets the requirement. unittest is adopted here. Also,
	there should be a testing report when complete automation, HTMLTestRunner is a wonderful tool. 

Precondition:
	The platform is base on Andriod platform, debug on windows system, but it may be availabe on Linux.
	Before build the project, make sure you have:
	1.python3
	2.adb tool
	3.unittest
	4.HTMLTestRunner
	5.uiautomator2
	6.atx-agent
	7.uiautomator apk
	8.Fiddler if you want to capture the app api
	

1.Configure adb
	you could download the adb tool on the website, but make sure it is suitable for your systme(windows, linux or mac os).if your system is windows, you could see the tool you want under the diretory 'tools'
	under the project. Then please configure as system environment.
	
2.Install weditor
	weditor is a tool to capture the app element so that we could easy to develop test script. It is stable and convienient.
	please install as below:
		pip install --pre weditor
		
	run command: python -m weditor
	
	if not any error raise, it means install successful. 

2.Install unittest
	pip install unittest

3.Install HTMLTestRunner
	pip install html-testRunner

4.Install uiautomator2
	# Since uiautomator2 is still under development, you have to add --pre to install the development version
	pip install --upgrade --pre uiautomator2

	# Or you can install directly from github source
	git clone https://github.com/openatx/uiautomator2
	pip install -e uiautomator2

5.Install apk and atx-agent
	there are two ways to install the apk and atx-agent:
	(1): push the apk and atx-agent to phone, execute command:
		python -m uiautomator2 init
		adb push atx-agent /data/local/tmp
		adb shell chmod 755 /data/local/tmp/atx-agent
		#launch atx-agent in daemon mode
		adb shell /data/local/tmp/atx-agent server -d

	(2): i have write a script to install, just 'python env_install.py', code as below:
		import os
		import re

		cur_path = os.path.dirname(os.path.abspath(__file__))

		env_path = os.path.join(cur_path,'tools')

		uiautomator_apk = os.path.join(env_path,'app-uiautomator-androidx.apk')
		uiautomator_text_apk = os.path.join(env_path,'app-uiautomator-test-androidx.apk')

		atx_agent = os.path.join(env_path,'atx-agent','atx-agent')

		# consider multiple devices
		devices = [re.match(r'^(\w+)\t',device)[1] for device in os.popen('adb devices').readlines() if re.match(r'^\w+\t',device) ]

		# env configure and installation
		for d in devices:
			os.system("adb -s {} {}".format(d,uiautomator_apk))
			os.system("adb -s {} {}".format(d,uiautomator_text_apk))
			os.system("adb -s {} push {} /data/local/tmp".format(d,atx_agent))
			# chmod 
			os.system("adb -s {} shell chmod 755 /data/local/tmp/atx-agent".format(d))
			os.system("adb -s {} shell /data/local/tmp/atx-agent server -d".format(d))
		print('initial apk and atx-agent success')
		
6.Download and install Fiddler
	please refer to https://www.telerik.com/fiddler.


7.About atx-agent
	if you need more infomation, please refer to https://github.com/openatx/atx-agent

8.About uiautomator2
	if you need more infomation, please refer to https://github.com/xiaocong/uiautomator
	
	an simple for how to use uiautomator2
	There are two ways to connect to the device.
	Through WiFi
	Suppose device IP is 10.0.0.1 and your PC is in the same network.

	import uiautomator2 as u2

	d = u2.connect('10.0.0.1') # alias for u2.connect_wifi('10.0.0.1')
	print(d.info)
	
	Through USB
	Suppose the device serial is 123456f (seen from adb devices)

	import uiautomator2 as u2

	d = u2.connect('123456f') # alias for u2.connect_usb('123456f')
	print(d.info)
	Through ADB WiFi
	import uiautomator2 as u2

	d = u2.connect_adb_wifi("10.0.0.1:5555")
	Calling u2.connect() with no argument, uiautomator2 will obtain device IP from the environment variable ANDROID_DEVICE_IP or ANDROID_SERIAL. If this environment variable is empty, uiautomator will fall back to connect_usb and you need to make sure that there is only one device connected to the computer.


* Task1: App UI Automation
	an expample is :
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
			
* Taks2: Api Capture and Send Request
	base on python+uiautomator2+fiddler
	1. install fiddler
		refer before step
		
	2.configure fiddler
		allow https; configure port as 8888; allow external connection; ensure phone and PC are shared the same network
		
	3.find the api via fiddler
	
	4.capture and send request via python
