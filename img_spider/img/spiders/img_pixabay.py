import json
import re
import os
import requests

from scrapy import Spider, Request
from pyquery import PyQuery as pq
from ..items import ImgItem
from ..get_words import read_keywords_list
from json import loads
import urllib.parse


class ImgspiderSpider(Spider):
    name = "img_pixabay"

    def __init__(self, *args, **kwargs):
        self.allowed_domains = ["pixabay.com"]
        self.headers = {
            'Accept': "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
            'Accept-Language': "en-US,en;q=0.9",
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'cookie': '__cfduid = d9efff7c4dd6d4336a55290f505e5ae211568683206;_ga = GA1.2.1646761631.1568683208;_gid = GA1.2.464847544.1568683208;is_human = 1;lang = zh;csrftoken = edxF4q8bBb3oAoItPNX4ZFDRAVwRBjEnczM5bxmVie514LjXYWVSx9etGHAlPueR;sessionid = ".eJxVjEsOgyAUAO_CujGK8qC9DHngq9ACNnw2Nr17rYsmbicz82Y6YFoaLsRubHPswjS26nQrlLXD4nYMCtUdJyFm1Q9yNKiMGAAEgQSQiksCCz3xc2zQPinNe__K64Ns7Vr1oXS2lbrGQ-z8oSaMpNesKaIP_-4087_PMMJ0HXvOPl-VKT0l:1iA2Pg:YhbVSZ_qtIrQZMm5ai3P6Atf6V4";client_width = 1208'

        }

    def start_requests(self):
        keywords = read_keywords_list()
        # keywords = ['sleep', 'cry']
        pages = 180

        for keyword in keywords:
            c = 0
            for ch in keyword:
                if u'\u4e00' <= ch <= u'\u9fff':
                    c = c + 1
            if c == 0:
                for page_num in range(1, pages):

                    url = 'https://pixabay.com/images/search/{keyword}/?cat=people&pagi={pages}'.format(keyword=keyword, pages=page_num)

                    yield Request(url=url, callback=self.parse)

    def parse(self, response):
        pattern = re.compile(r'1x, (.*?) 2x"')
        img_list = re.findall(pattern, response.text)
        img_item = ImgItem()
        link = 'https://pixabay.com/zh/images/download/'
        for img_url in img_list:
            # img_item['img_url'] = link + img_url.rpartition('/')[2].split('__')[0] + '.jpg'
            # # print(img_item['img_url'])
            # img_item['img_website'] = self.name.split('_')[-1]
            # img_item['img_name'] = img_url.rpartition('/')[2].split('__')[0] + '.jpg'
            url = link + img_url.rpartition('/')[2].split('__')[0] + '.jpg'
            with open(os.path.join(r'D:\scrapy_down', 'pixabay1.txt'), 'a') as fp:
                fp.write(str(url))
                fp.write('\n')
            # yield img_item
            # try:
            #     res = requests.get(img_item['img_url'], headers=self.headers)
            #     print('正在请求图片链接...')
            #     if res.status_code == 200:
            #         with open('D:\\new_img\\' + img_item['img_name'], 'wb') as fp:
            #             fp.write(res.content)
            # except Exception as e:
            #     print(e)
            #     print('图片下载失败，链接已存入lost_url中......')
