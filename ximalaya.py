import requests
import time
import hashlib
import random
import json

# 爬取喜马拉雅的音乐的类
class ximalaya(object):

    def __init__(self, url):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36"
        }
        self.url = url

    def getServerTime(self):
        """
        获取喜马拉雅服务器的时间戳
        :return:
        """
        # 这个地址就是返回服务器时间戳的接口
        serverTimeUrl = "https://www.ximalaya.com/revision/time"
        response = requests.get(serverTimeUrl,headers = self.headers)
        return response.text

    def getSign(self,serverTime):
        """
        生成 xm-sign
        规则是 md5(ximalaya-服务器时间戳)(100以内随机数)服务器时间戳(100以内随机数)现在时间戳
        :param serverTime:
        :return:
        """
        nowTime = str(round(time.time()*1000))

        sign = str(hashlib.md5("ximalaya-{}".format(serverTime).encode()).hexdigest()) + "({})".format(str(round(random.random()*100))) + serverTime + "({})".format(str(round(random.random()*100))) + nowTime
        # 将xm-sign添加到请求头中
        self.headers["xm-sign"] = sign
        # return sign

    def getInfos(self):
        # 先调用该方法获取xm-sign
        self.getSign(self.getServerTime())
        # 将访问数据接口的参数写好
        # 喜马拉雅数据接口
        # url = "https://www.ximalaya.com/revision/play/album?albumId=19492295&pageNum=1&sort=1&pageSize=30"
        response = requests.get(self.url, headers=self.headers)
        infos = json.loads(response.text)
        # print(infos)
        return infos

if __name__ == '__main__':
    ximalaya = ximalaya('https://www.ximalaya.com/revision/play/album?albumId=19492295&pageNum=1&sort=1&pageSize=30')
    ximalaya.getInfos()