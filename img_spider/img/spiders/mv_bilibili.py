from scrapy import Spider,Request

from ..get_words import read_keywords_list
from pyquery import PyQuery as pq
from ..items import MvItem
from scrapy.conf import settings
import pymysql
import youtube_dl


class ImgspiderSpider(Spider):
    name = "mv_bilibili"
    allowed_domains = ["bilibili.com"]
    id = 20000


    def start_requests(self):
        keywords = read_keywords_list()
        # keywords = ['打篮球']
        pages = 4

        for keyword in keywords:
            for page_num in range(1, pages):
                url = 'https://search.bilibili.com/video?keyword={keyword}&from_source=banner_search&order=totalrank&duration=0&tids_1=0&page={pages}'.format(pages=page_num, keyword=keyword)

                yield Request(url=url, callback=self.parse, meta={'num': keyword})

    def parse(self, response):
        keyword = response.meta['num']
        html = response.text
        doc = pq(html)
        url_item = doc('.video.matrix a').items()
        file = keyword
        path = r'C:\Users\pph\Desktop\mv\{}'.format(file)
        for url in url_item:
            v_url = 'https:' + url.attr('href')
            try:
                ydl_opts = {'outtmpl': '{}/%(title)s.%(ext)s'.format(path)}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.extract_info(v_url)
            except Exception as e:
                print('download failed:', v_url)
                print(e)


