'''
%7B%22blocks%22%3A%5B%7B%22block%22%3A%22serp-controller%22%2C%22params%22%3A%7B%7D%2C%22version%22%3A2%7D%2C%7B%22block%22%3A%22serp-list_infinite_yes%22%2C%22params%22%3A%7B%22initialPageNum%22%3A0%7D%2C%22version%22%3A2%7D%2C%7B%22block%22%3A%22more_direction_next%22%2C%22params%22%3A%7B%7D%2C%22version%22%3A2%7D%2C%7B%22block%22%3A%22gallery__items%3Aajax%22%2C%22params%22%3A%7B%7D%2C%22version%22%3A2%7D%5D%2C%22bmt%22%3A%7B%22lb%22%3A%22KI9Ja%3D52Fx%22%7D%2C%22amt%22%3A%7B%22las%22%3A%22%22%7D%7D

%7B%22blocks%22%3A%5B%7B%22block%22%3A%22serp-controller%22%2C%22params%22%3A%7B%7D%2C%22version%22%3A2%7D%2C%7B%22block%22%3A%22serp-list_infinite_yes%22%2C%22params%22%3A%7B%22initialPageNum%22%3A0%7D%2C%22version%22%3A2%7D%2C%7B%22block%22%3A%22more_direction_next%22%2C%22params%22%3A%7B%7D%2C%22version%22%3A2%7D%2C%7B%22block%22%3A%22gallery__items%3Aajax%22%2C%22params%22%3A%7B%7D%2C%22version%22%3A2%7D%5D%2C%22bmt%22%3A%7B%22lb%22%3A%22KI9Ja%3D52Fx%22%7D%2C%22amt%22%3A%7B%22las%22%3A%22%22%7D%7D
'''

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
    name = "img_aol"

    def __init__(self, *args, **kwargs):
        self.allowed_domains = ["search.aol.com"]

    def start_requests(self):
        keywords = read_keywords_list()
        pages = 50

        for keyword in keywords:

            for page_num in range(1, pages):
                page_num = (page_num-1)*60 + 1



                url = 'https://search.aol.com/aol/image?q={keyword1}&n=60&ei=UTF-8&y=Search&s_it=sb_top&v_t=na&o=js&p={keyword2}&tmpl=&nost=1&b={pages}&ig=0afd1ebed72e416ba500000000ab40d1&rand=1555569649824'.format(keyword1=keyword, keyword2=keyword, pages= page_num)
                print(url)
                # url = 'https://search.aol.com/aol/image?q=%E8%BA%BA&n=60&ei=UTF-8&y=Search&s_it=sb_top&v_t=na&o=js&p=%E8%BA%BA&tmpl=&nost=1&b=1&ig=0afd1ebed72e416ba500000000ab40d1&rand=1555569649824'

                yield Request(url=url, callback=self.parse)

    def parse(self, response):
        # self.cookie = response.request.headers.getlist('Cookie')
        # print(response.text)
        pattern = re.compile(r'\\"iurl\\":\\"(.*?)\\"')
        img_list = re.findall(pattern, response.text)
        # img_item = ImgItem()
        for i in img_list:
            b = i.split('\\')
            s = ''
            for i in b:
                s = s + i
            img_url = s
            img_item = ImgItem()
            print(img_url)
            img_item['img_url'] = img_url
            img_item['img_website'] = self.name.split('_')[-1]
            img_item['img_name'] = img_url.split('/')[-1]
            yield img_item

