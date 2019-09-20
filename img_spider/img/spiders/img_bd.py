# -*- coding: utf-8 -*-

import json

from scrapy import Spider, Request
from ..items import ImgItem
from ..get_words import read_keywords_list

def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def get_keyword(row_words):
    keywords = []
    for row_word in row_words:
        if check_contain_chinese(row_word) == True:
            keywords.append(row_word)
    return keywords

class ImgspiderSpider(Spider):
    name = "img_bd"

    def __init__(self, *args, **kwargs):
        self.allowed_domains = ["image.baidu.com", "www.baidu.com", 'ss3.bdstatic.com', 'ss2.bdstatic.com',
                                'ss1.bdstatic.com', 'ss0.bdstatic.com']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'
    }

    def start_requests(self):

        row_words = read_keywords_list()
        keywords = get_keyword(row_words)

        urls = [
            'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord+={0}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&word={0}&z=&ic=0&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&step_word={0}&pn={1}&rn=60&gsm=1e&1528441524820='.format(
                keyword, page * 60) for keyword in keywords for page in range(0, 401)]
        for url in urls:
            yield Request(url, headers=self.headers)

    def parse(self, response):
        img_items = json.loads(response.body)['data']
        for img_single in img_items:
            if 'middleURL' in list(img_single.keys()):
                img_url = img_single['middleURL']
                if img_url != "":
                    img_item = ImgItem()
                    print(img_url)
                    img_item['img_url'] = img_url
                    img_item['img_website'] = self.name.split('_')[-1]
                    img_item['img_name'] = img_url.split('/')[-1]
                    yield img_item