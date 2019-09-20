from scrapy import Spider,Request
from json import loads
import json
from ..get_words import read_keywords_list
from pyquery import PyQuery as pq
from ..items import ImgItem
import os
import requests


class ImgspiderSpider(Spider):
    name = "img_paixin"
    allowed_domains = ["v.paixin.com"]
    # start_urls = ['https://dpapi.dispatch.paixin.com/search_list?limit=42&line={}'.format(i*42) for i in range(0,101)]
    # data = {
    #     'color':"0",
    #     'keyword':"躺",
    #     'type':"6",
    # }
    # scrapy crawl imgspider

    def start_requests(self):
        keywords = read_keywords_list()
        pages = 60

        for keyword in keywords:
            data = {
                'color': "0",
                'keyword': keyword,
                'type': "6",
            }
            for page_num in range(1, pages):
                url = 'https://dpapi.dispatch.paixin.com/search_list?limit=52&line={}'.format((page_num-1)*52)
                headers = {
                    'Accept': "'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'",
                    'Accept-Language': "en",
                    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
                    'content-type': 'application/json'
                }
                yield Request(url=url, headers=headers, method='POST', body=json.dumps(data), callback=self.parse)



    def parse(self, response):
        model_dict = loads(response.text)
        img_item = ImgItem()
        for img in model_dict['data']:
            img_url = img['image2']# image2 为带水印的大图
            # print(img_url)

            img_url = requests.get(img_url).url
            print(img_url)
            img_item['img_url'] = img_url
            img_item['img_website'] = self.name.split('_')[-1]
            img_item['img_name'] = img_url.split('/')[-3] + img_url.split('/')[-2] + img_url.split('/')[-1]
            yield img_item

