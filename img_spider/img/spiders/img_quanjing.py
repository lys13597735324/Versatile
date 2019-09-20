from scrapy import Spider,Request
from json import loads
import json
from ..get_words import read_keywords_list
from pyquery import PyQuery as pq
from ..items import ImgItem
import os
import requests
import re

class ImgspiderSpider(Spider):
    name = "img_quanjing"
    allowed_domains = ["quanjing.com"]

    def start_requests(self):
        keywords = read_keywords_list()
        pages = 100

        for keyword in keywords:

            for page_num in range(1, pages):
                url = 'https://www.quanjing.com/Handler/SearchUrl.ashx?t=1360&callback=searchresult&q={keyword}&stype=1&pagesize=100&pagenum={page}&imageType=2&imageColor=&brand=&imageSType=&fr=1&sortFlag=1&imageUType=&btype=&authid=&_=1555741341019'.format(keyword=keyword, page=page_num)
                headers = {
                    'Accept': "'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'",
                    'Accept-Language': "zh-CN,zh;q=0.9",
                    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
                    'content-type': 'application/json',
                    'referer': 'https://www.quanjing.com/search.aspx?q=%E8%BA%BA'

                }
                yield Request(url=url, headers=headers, callback=self.parse)



    def parse(self, response):
        # print(response.text)
        pattern = re.compile(',"imgurl":"(.*?)","imgCode":')
        img_list = re.findall(pattern, response.text)
        img_item = ImgItem()
        for img_url in img_list:
            img_item['img_url'] = img_url
            img_item['img_website'] = self.name.split('_')[-1]
            img_item['img_name'] = img_url.split('/')[-1]
            yield img_item