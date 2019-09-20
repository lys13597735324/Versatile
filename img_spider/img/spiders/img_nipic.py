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
    name = "img_nipic"

    def __init__(self, *args, **kwargs):
        self.allowed_domains = ["nipic.com"]

    def start_requests(self):
        keywords = read_keywords_list()
        # keywords = ['睡着的小孩']
        pages = 150

        for keyword in keywords:
            # c = 0
            # for ch in keyword:
            #     if u'\u4e00' <= ch <= u'\u9fff':
            #         c = c + 1
            # if c == 0:
            for page_num in range(1, pages):
                url = 'http://soso.nipic.com/?q={keyword}&g=0&page={pages}'.format(keyword=keyword, pages=page_num)
                yield Request(url=url, callback=self.parse)

    def parse(self, response):
        # print(response.text)
        # print(type(response.text))
        html = response.text
        doc = pq(html)
        url_item = doc('.clearfix .new-search-works-item a img').items()
        img_Item = ImgItem()
        for url in url_item:
            img_url = url.attr('data-original')
            n = img_url.split('.')[-2][-1]
            if n == '4':
                img_url = img_url.replace('pic/', '')
                img_url = img_url.replace('_4.jpg', '_2.jpg')
            elif n == '0':
                img_url = img_url.replace('pic/', 'res/')
                img_url = img_url.replace('_0.jpg', '_1.jpg')
            if img_url != None:
                    img_Item['img_url'] = img_url
                    img_Item['img_website'] = self.name.split('_')[-1]
                    img_Item['img_name'] = img_url.split('/')[-1]
                    yield img_Item

