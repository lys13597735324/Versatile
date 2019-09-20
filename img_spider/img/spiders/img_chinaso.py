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
    name = "img_chinaso"

    def __init__(self, *args, **kwargs):
        self.allowed_domains = ["chinaso.com"]

    def start_requests(self):
        keywords = read_keywords_list()
        # keywords = ['躺下', '睡觉']
        pages = 80

        for keyword in keywords:

            for page_num in range(1, pages):
                page_num = (page_num - 1)*72

                url = 'http://image.chinaso.com/getpic?rn=72&st={page}&q={keyword}&t=1555900779750'.format(page=page_num, keyword=keyword)
                print(url)


                yield Request(url=url, callback=self.parse)

    def parse(self, response):
        model_dict = loads(response.text)
        img_item = ImgItem()
        for img in model_dict['arrResults']:
            img_url = img['url']
            img_item['img_url'] = img_url
            # print(img_url)
            img_item['img_website'] = self.name.split('_')[-1]
            img_item['img_name'] = img_url.split('/')[-1]
            yield img_item