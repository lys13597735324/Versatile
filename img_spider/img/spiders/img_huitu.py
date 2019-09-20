import json
import re
import requests

from scrapy import Spider, Request
from pyquery import PyQuery as pq
from ..items import ImgItem
from ..get_words import read_keywords_list
from json import loads
import urllib.parse


class ImgspiderSpider(Spider):
    name = "img_huitu"

    def __init__(self, *args, **kwargs):
        self.allowed_domains = ["huitu.com"]

    def start_requests(self):
        keywords = read_keywords_list()
        # keywords = ['躺下', '睡觉']
        pages = 100

        for keyword in keywords:

            for page_num in range(1, pages):

                url = 'http://soso.huitu.com/Search/GetAllPicInfo?perPageSize=102&kw={keyword}&page={page}&tp=0'.format(page=page_num, keyword=keyword)
                print(url)


                yield Request(url=url, callback=self.parse)

    def parse(self, response):
        model_dict = loads(response.text)
        img_item = ImgItem()
        for img in model_dict['r']:
            img_url = img['imgBigUrl']
            img_item['img_url'] = img_url
            # print(img_url)
            img_item['img_website'] = self.name.split('_')[-1]
            img_item['img_name'] = img_url.split('/')[-1]
            yield img_item