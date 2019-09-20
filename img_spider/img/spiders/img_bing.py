# -*- coding: utf-8 -*-

from json import loads

from scrapy import Spider, Request
from pyquery import PyQuery as pq
from ..items import ImgItem
from ..get_words import read_keywords_list

class ImgspiderSpider(Spider):
    name = "img_bing"
    # allowed_domains = ["image.so.com"]



    def __init__(self, *args, **kwargs):
        self.allowed_domains = ["cn.bing.com"]

    def start_requests(self):

        keywords = read_keywords_list()
        pages = 30
        for keyword in keywords:
            for page in range(1, pages):
                page = (page-1)*26

                url = 'https://cn.bing.com/images/api/custom/search?q={keyword}&id=4EBD0A96425B29767A984789BEFEAEAA894A366C&preserveIdOrder=1&count=25&offset={page}&skey=o_1J4WsuIpQnXbGESTH9-FP5UfY82Rs7aAtLsqe_Zkc&safeSearch=Strict&mkt=zh-cn&setLang=zh-cn&IG=21103D4DCAD14176955D5CAC2E08D53E&IID=idpfs&SFX=1'.format(keyword=keyword, page=page)
                default_headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
                'referer': 'https://cn.bing.com/images/search?view=detailV2&ccid=NEA6UbeR&id=4EBD0A96425B29767A984789BEFEAEAA894A366C&thid=OIP.NEA6UbeRSvAfPUTlHHRVwwHaLE&mediaurl=http%3A%2F%2Fwww.zhlzw.com%2Fsj%2FUploadFiles_9645%2F201210%2F20121029123936827.jpg&exph=2242&expw=1500&q={}&simid=607986313550565257&selectedindex=0&ajaxhist=0&vt=0'.format(keyword),
                'cookie': 'MMCA=ID=81D193A22F7243C28E7AD18924F7621E; _IDET=NVNoti=1; ipv6=hit=1555646987765&t=4; MUID=35C50AAD351264C92167065F34B9654F; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=748766202D9344C2B4792F902296AFD1&dmnchg=1; MUIDB=35C50AAD351264C92167065F34B9654F; _ITAB=STAB=TR; SRCHUSR=DOB=20190129&T=1555643299000; _EDGE_S=mkt=zh-cn&ui=zh-cn&SID=025F106CE11B68F4046A1D2FE0356904; _SS=SID=025F106CE11B68F4046A1D2FE0356904&HV=1555643390; SRCHHPGUSR=CW=1903&CH=458&DPR=1&UTC=480&WTS=63691240099'
            }
                yield Request(url=url, callback=self.parse,headers=default_headers)

    def parse(self, response):
        model_dict = loads(response.text)
        img_item = ImgItem()
        for img in model_dict['value']:
            img_url = img['contentUrl']  # image2 为带水印的大图
            print(img_url)
            img_item['img_url'] = img_url
            img_item['img_website'] = self.name.split('_')[-1]
            img_item['img_name'] = img_url.split('/')[-1]
            yield img_item




