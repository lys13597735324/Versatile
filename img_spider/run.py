import sys
import os
import time
from scrapy.cmdline import execute
import os
os.system("scrapy crawl img_360")
time.sleep(300)
os.system("scrapy crawl img_bd")
time.sleep(300)
os.system("scrapy crawl img_bing")
# time.sleep(300)
# os.system("scrapy crawl img_veer")