from scrapy import Spider,Request

from ..get_words import read_keywords_list
from pyquery import PyQuery as pq
from ..items import MvItem
from scrapy.conf import settings
import pymysql
import youtube_dl


class ImgspiderSpider(Spider):
    name = "mysql_mv_bilibili"
    allowed_domains = ["bilibili.com"]
    id = 20000


    def start_requests(self):
        keywords = read_keywords_list()
        # keywords = ['打篮球']
        pages = 2

        for keyword in keywords:
            for page_num in range(1, pages):
                url = 'https://search.bilibili.com/all?keyword={keyword}&from_source=banner_search&order=totalrank&duration=0&tids_1=160&tids_2=21&page={pages}'.format(pages=page_num, keyword=keyword)

                yield Request(url=url, callback=self.parse, meta={'num': keyword})

    def parse(self, response):
        connect = pymysql.connect(
            host=settings['MYSQL_HOST'],
            port=3306,
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True)
        # 通过cursor执行增删查改
        cursor = connect.cursor()

        keyword = response.meta['num']
        html = response.text
        # print(html)
        doc = pq(html)
        url_item = doc('.headline.clearfix a').items()
        file = keyword
        path = r'C:\Users\pph\Desktop\mv\{}'.format(file)
        # print(path)
        video_item = MvItem()
        for url in url_item:
            v_url = 'https:' + url.attr('href')
            print(v_url)
            v_name = url.attr('title')
            try:
                # 查重处理
                cursor.execute(
                    """select * from pmv_video where url = %s""",
                    v_url.split('?')[0])
                # 是否有重复数据
                repetition = cursor.fetchone()
                #重复
                if repetition == None:

                    try:
                        ydl_opts = {'outtmpl': '{}/%(title)s.%(ext)s'.format(path)}
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            video = ydl.extract_info(v_url)
                        title = v_name + '.' + video['ext']
                        # print(title)
                        video_item['id'] = self.id
                        video_item['keyword'] = keyword
                        video_item['url'] = v_url.split('?')[0]
                        video_item['title'] = title
                        video_item['rename'] = 'PM_' + str(self.id).zfill(6)
                        self.id += 1
                    except Exception as e:
                        print('download failed:', v_url)
                        print(e)
            except Exception as e:
                # 出现错误时打印错误日志
                print(e)
            yield video_item