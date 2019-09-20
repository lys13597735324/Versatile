import requests
from ximalaya import ximalaya
import os
from multiprocessing import Pool, Queue


# page = 14
# for i in range(11, page):
#     url = 'https://www.ximalaya.com/revision/play/album?albumId=14495260&pageNum={}&sort=0&pageSize=30'.format(i)
#     print(url)
#     fm = ximalaya(url)
#     data = fm.getInfos()
#     for m4a in data['data']['tracksAudioPlay']:
#         print(m4a['src'])
#         print(m4a['trackName'])
#         print(m4a['trackId'])
#         if os.path.exists(os.path.join(r'D:\scrapy_down\14495260', m4a['trackName'] + str(m4a['trackId']) + '.m4a')) ==False:
#             resp = requests.get(url=m4a['src'])
#             with open(os.path.join(r'D:\scrapy_down\14495260', m4a['trackName'] + str(m4a['trackId']) + '.m4a'), 'wb') as fp:
#                 fp.write(resp.content)


def create_url_queue(keynumber, q):
    pages = 14
    for i in range(11, pages):
        url = 'https://www.ximalaya.com/revision/play/album?albumId={keynumber}&pageNum={page}&sort=0&pageSize=30'\
            .format(keynumber=keynumber, page=i)
        q.put(url)
    return q


def downloads(url, result_path):
    try:
        fm = ximalaya(url)
        data = fm.getInfos()
        for m4a in data['data']['tracksAudioPlay']:
            print('正在请求链接', m4a['src'])
            if os.path.exists(
                    os.path.join(result_path, m4a['trackName'] + str(m4a['trackId']) + '.m4a')) == False:
                resp = requests.get(url=m4a['src'])
                with open(os.path.join(result_path, m4a['trackName'] + str(m4a['trackId']) + '.m4a'),
                          'wb') as fp:
                    fp.write(resp.content)
                    print('success', m4a['trackName'] + str(m4a['trackId']) + '.m4a')
    except Exception as e:
        print(e)
        print('下载失败')



if __name__ == '__main__':
    result_path = r'D:\scrapy_down\001'
    keynumber = 14495260
    q = Queue()
    row_url = create_url_queue(keynumber, q)
    p = Pool(4)
    while True:
        if row_url.empty() == False:
            p.apply_async(downloads, args=(row_url.get(), result_path))
        else:
            break
    p.close()
    p.join()