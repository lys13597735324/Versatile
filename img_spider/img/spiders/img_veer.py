# -*- coding: utf-8 -*-

from scrapy import Spider, FormRequest
import requests
import json

from ..items import ImgItem
from ..get_words import read_keywords_list

def post_json(url, keyword, page=1):
    payload = "{\"graphicalStyle\":\"1\",\"phrase\":\"%s\",\"key\":\"8G6AH\",\"page\":%s,\"perpage\":100,\"changeTitle\":\"搜索结果 - Veer图库_全球领先的正版商业图片素材交易平台\",\"page_type\":6,\"anonyUid\":\"1K2BD0DE1J1K\",\"favorid\":\"\"}" % (
        keyword, page)
    response = requests.request("POST", url, data=payload.encode('utf8'), headers=headers)
    content = json.loads(response.text)
    total_count = content['data']['totalCount']
    return total_count


# 请求头
headers = {
    'Content-Type': "application/json",
    'Accept': "*/*",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Content-Length': "222",
    'Cookie': "acw_tc=276aedd215415590576737234e64570d48282a72e5ecdc0e59152123ae8359; sajssdk_2015_cross_new_user=1; Hm_lvt_f2de34005a64c75f44715498bcb136f9=1541559059; _ga=GA1.2.228814768.1541559059; _gid=GA1.2.588353651.1541559059; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22278028%22%2C%22%24device_id%22%3A%22166ec147e595e8-006be9a5abe855-1e386652-1296000-166ec147e5b3d7%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22166ec147e595e8-006be9a5abe855-1e386652-1296000-166ec147e5b3d7%22%7D; st=VEER-ST-278028-378-c7f04e948d4b434989438c6a4a19670c; uid=278028; ticket=6B7E8DE33C6F30B8D33116BDBA3784295EA0C28A98E7F4838E40F7FD429A3CE385B0606DA9542705E02E446774B2709F; name=ngchang; mobile=157****7039; payStatus=0; Hm_lpvt_f2de34005a64c75f44715498bcb136f9=1541571651; _gat=1",
    'DNT': "1",
    'Host': "www.veer.com",
    'Origin': "https://www.veer.com",
    'Pragma': "no-cache",
    'Referer': "https://www.veer.com/",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    'cache-control': "no-cache",
    'Postman-Token': "2ab4c03b-8bb4-49d0-a83e-47826d7ac8e9"
}


class ImgspiderSpider(Spider):
    name = "img_veer"

    def __init__(self, *args, **kwargs):
        self.allowed_domains = ["goss.veer.com", "goss0.veer.com", "goss1.veer.com", "goss2.veer.com", "goss3.veer.com",
                                "goss4.veer.com", "goss5.veer.com", "www.veer.com"]

    def start_requests(self):
        url = "https://www.veer.com/ajax/search"
        count = 0
        keywords = read_keywords_list()
        for keyword in keywords:
            total_count = post_json(url, keyword)
            # 100 为真实页数 1000为前10%
            total_page = total_count // 1000 + 1
            print(count)
            for page in range(0, total_page):
                payload = {"graphicalStyle": "1", "phrase": keyword, "key": "8G6AH", "page": str(page), "perpage": "100",
                           "changeTitle": "搜索结果 - Veer图库_全球领先的正版商业图片素材交易平台", "page_type": "6", "anonyUid": "1K2BD0DE1J1K",
                           "favorid": ""}
                count += 100
                # yield FormRequest(url, callback=self.after_post, method='POST', headers=headers, formdata=payload)
                yield FormRequest(url, callback=self.parse, formdata=payload)

    def parse(self, response):
        content = json.loads(response.text)
        row_list = content['data']['list']
        img_item = ImgItem()
        for single_dict in row_list:
            img_url = single_dict['oss400']
            # id = single_dict['id']
            img_item['img_url'] = img_url
            img_item['img_website'] = self.name.split('_')[-1]
            img_item['img_name'] = img_url.split('/')[-1]
            yield img_item

