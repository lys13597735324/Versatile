# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import socket

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
import requests
import pymysql
from .settings import IMAGES_STORE
from scrapy.conf import settings

# host: localhost / 127.0.0.1 / 192.168.188.39 / 192.168.0.120
# db_info = {"host": "192.168.0.113", "user": "root", "password": "Ast12@Ljh", "db": "crawl_url_record"}
db_info = {"host": "localhost", "user": "root", "password": "IDqCM@mysql", "db": "crawl_url_record"}


class ImgPipeline(object):
    def process_item(self, item, spider):
        return item


class ImgDownloadPipeline(ImagesPipeline):
    default_headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        'cookie': '__cfduid = d9efff7c4dd6d4336a55290f505e5ae211568683206;_ga = GA1.2.1646761631.1568683208;_gid = GA1.2.464847544.1568683208;is_human = 1;lang = zh;csrftoken = edxF4q8bBb3oAoItPNX4ZFDRAVwRBjEnczM5bxmVie514LjXYWVSx9etGHAlPueR;sessionid = ".eJxVjEsOgyAUAO_CujGK8qC9DHngq9ACNnw2Nr17rYsmbicz82Y6YFoaLsRubHPswjS26nQrlLXD4nYMCtUdJyFm1Q9yNKiMGAAEgQSQiksCCz3xc2zQPinNe__K64Ns7Vr1oXS2lbrGQ-z8oSaMpNesKaIP_-4087_PMMJ0HXvOPl-VKT0l:1iA2Pg:YhbVSZ_qtIrQZMm5ai3P6Atf6V4";client_width = 1208'

    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }
    #  使用ImagePipeline组件下载图片的时候，图片名称是以图片URL的SHA1值进行保存的。
    #  重写file_path代替image_key函数。
    def file_path(self, request, response=None, info=None):
        if request.url.split('/')[-1] == 'staff_1024.jpg':
            image_guid = request.url.split('/')[-3] + request.url.split('/')[-2] + request.url.split('/')[-1]
        else:
            image_guid = request.url.split('/')[-1]
        print(image_guid)
        return '%s' % (image_guid)

    # item['image_urls']是我们在item.py中定义的存放图片url的变量，如果定义了别的变量名，注意更换
    def get_media_requests(self, item, info):
        # if 'iplant.cn' in item['img_url']:
        #     headers = self.default_headers
        #     headers['referer'] = 'http://ppbc.iplant.cn'
        #     # self.default_headers['referer'] = 'http://ppbc.iplant.cn/tu' + str(os.path.splitext(os.path.basename(item['img_url'])))
        # if 'pixabay.com' in item['img_url']:
        #     respone = requests.get(item['img_url'], headers=self.default_headers, allow_redirects=False)
        #     print(respone.status_code)
        #     if respone.status_code == 302 or respone.status_code == 301:
        #         item['img_url'] = 'https://pixabay.com' + respone.headers['Location']
        #         # print(respone.headers['Location'])
        yield Request(item['img_url'], headers=self.headers)



    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contain no images")
        item['img_path'] = image_paths
        return item


class ImgInsertDbPipeline(object):

    def open_spider(self, spider):
        self.connect = pymysql.connect(
            host=db_info["host"],
            db=db_info["db"],
            user=db_info["user"],
            password=db_info["password"],
            cursorclass=pymysql.cursors.DictCursor
        )

    def close_spider(self, spider):
        self.connect.close()

    def process_item(self, item, spider):
        if item['img_url'] != '#':
            img_url = item['img_url']
            img_file_name = item['img_name'].split('/')[-1]
            # img_file_name = item['img_url'].split('/')[-1]
            img_website = item["img_website"]
            img_db_id = img_website + "_" + img_file_name.split('.')[0]
            img_store_path = os.path.join(IMAGES_STORE, "full")
            img_store_machine = socket.getfqdn(socket.gethostname())

            sql_insert = """INSERT INTO search_engine_record (db_id, website, file_name, url, store_machine, store_path) VALUES (%s, %s, %s, %s, %s, %s)"""

            try:
                # 通过cursor进行增删改查
                self.cursor = self.connect.cursor()
                with self.cursor as cursor_insert:
                    cursor_insert.execute(sql_insert, (
                        img_db_id, img_website, img_file_name, img_url, img_store_machine, img_store_path))
                self.connect.commit()
            except Exception as error:
                self.connect.rollback()
                print(error)
        return item

class DBPipeline(object):

    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host=settings['MYSQL_HOST'],
            port=3306,
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor();

    def process_item(self, item, spider):

        try:
            # 查重处理
            self.cursor.execute(
                """select * from pmv_video where url = %s""",
                item['url'])
            # 是否有重复数据
            repetition = self.cursor.fetchone()

            # 重复
            if repetition:
                pass

            else:
                # 插入数据
                self.cursor.execute(
                    """insert into pmv_video(id, keyword, url, title, renamed) value (%s, %s, %s, %s, %s)""",
                    (item['id'],
                     item['keyword'],
                     item['url'],
                     item['title'],
                     item['rename']))
                # print(item['rename'])
                # print(type(item['rename']))

            # 提交sql语句
            self.connect.commit()

        except Exception as error:
            # 出现错误时打印错误日志
            print(error)
        return item