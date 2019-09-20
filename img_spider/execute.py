from scrapy.cmdline import execute
execute(('scrapy,crawl_all').split(','))
# execute(('scrapy,crawl_all,--nolog').split(','))