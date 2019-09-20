from scrapy import Spider,Request
from json import loads
import json
from ..get_words import read_keywords_list
from pyquery import PyQuery as pq
from ..items import ImgItem
import os
import requests
import re
import youtube_dl


class ImgspiderSpider(Spider):
    name = "mv_youku"
    allowed_domains = ["youku.com"]


    def start_requests(self):
        keywords = read_keywords_list()
        # keywords = ['打篮球']
        pages = 15

        for keyword in keywords:
            for page_num in range(1, pages):
                url = 'https://so.youku.com/search_video/q_{keyword}?spm=a2h0k.11417342.pageturning.dpagenumber&f=1&lengthtype=1&aaid=5ef40140a2e96400701f83194ecf393d&timemore=0&timeless=10&pg={pages}'.format(pages=page_num, keyword=keyword)
                headers = {
                    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                    'Accept-Language': "zh-CN,zh;q=0.9",
                    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
                }
                yield Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        html = response.text
        # print(html)
        pattern = re.compile(r'target=\\"_blank\\"  href=\\"(.*?)\\"> ')
        url_list = list(set(re.findall(pattern, html)))
        # print(len(url_list))
        path = r'C:\Users\pph\Desktop\mv'
        for url in url_list:
            v_url = url
            try:
                ydl_opts = {'outtmpl': '{}/%(title)s.%(ext)s'.format(path)}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([v_url])
            except Exception as e:
                print('download failed:', v_url)
                print(e)

