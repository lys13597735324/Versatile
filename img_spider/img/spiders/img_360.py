# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from json import loads
from ..items import ImgItem
from ..get_words import read_keywords_list


class ImgspiderSpider(Spider):
    name = "img_360"

    default_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }

    def __init__(self, *args, **kwargs):
        self.allowed_domains = ["image.so.com"]

    def start_requests(self):
        keywords = read_keywords_list()
        urls = ['http://image.so.com/j?q={0}&src=srp&t=s&correct={0}&pn=60&ch=&sn={1}&sid=dd676b0b9affe1e66e15e91455807b24&ran=0&ras=0&cn=0&gn=0&kn=0'.format(keyword, page*30) for keyword in keywords for page in range(0, 200) ]
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        model_dict = loads(response.text)

        for img_single in model_dict['list']:
            if img_single:
                img_item = ImgItem()
                img_url = img_single['img']
                img_item['img_url'] = img_url
                img_item['img_website'] = self.name.split('_')[-1]
                img_item['img_name'] = img_url.split('/')[-1]
                # print(img_url)
                yield img_item



