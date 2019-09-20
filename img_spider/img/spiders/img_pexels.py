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
    name = "img_pexels"

    def __init__(self, *args, **kwargs):
        self.allowed_domains = ["pexels.com"]

    def start_requests(self):
        keywords = read_keywords_list()

        pages = 2

        for keyword in keywords:
            c = 0
            for ch in keyword:
                if u'\u4e00' <= ch <= u'\u9fff':
                    c = c + 1
            if c == 0:
                for page_num in range(1, pages):

                    url = 'https://www.pexels.com/search/{keyword}/?&seed=2019-04-18%2008%3A36%3A41%20%2B0000&page={pages}&type='.format(keyword=keyword, pages=page_num)

                    yield Request(url=url, callback=self.parse)

    def parse(self, response):
        # print(response.text)
        # print(type(response.text))
        html = response.text
        doc = pq(html)
        img_item = doc('.photos__column .js-photo-link.photo-item__link img').items()
        img_Item = ImgItem()
        for img in img_item:
            img_url = img.attr('data-large-src')
            print(img_url)
            if img_url != None:
                img_Item['img_url'] = img_url.split('?')[0]
                print(img_Item['img_url'])
                img_Item['img_website'] = self.name.split('_')[-1]
                img_Item['img_name'] = img_url.split('/')[-1].split('?')[0]
                yield img_Item
