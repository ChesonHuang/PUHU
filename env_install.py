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
