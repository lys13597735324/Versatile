import requests
import os
from multiprocessing import Pool, Queue



def read_url(url_path, q):
    row_url = []
    with open(url_path, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            if line[-1] == "\n":
                row_url.append(line[0:-1])
            else:
                row_url.append(line)
    row_url = list(set(row_url))
    for i in row_url:
        q.put(i)
    return q


def downloads(url, result_path):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
        'cookie': '__cfduid = d9efff7c4dd6d4336a55290f505e5ae211568683206;_ga = GA1.2.1646761631.1568683208;_gid = GA1.2.464847544.1568683208;is_human = 1;lang = zh;csrftoken = edxF4q8bBb3oAoItPNX4ZFDRAVwRBjEnczM5bxmVie514LjXYWVSx9etGHAlPueR;sessionid = ".eJxVjEsOgyAUAO_CujGK8qC9DHngq9ACNnw2Nr17rYsmbicz82Y6YFoaLsRubHPswjS26nQrlLXD4nYMCtUdJyFm1Q9yNKiMGAAEgQSQiksCCz3xc2zQPinNe__K64Ns7Vr1oXS2lbrGQ-z8oSaMpNesKaIP_-4087_PMMJ0HXvOPl-VKT0l:1iA2Pg:YhbVSZ_qtIrQZMm5ai3P6Atf6V4";client_width = 1208',

    }
    if os.path.exists(os.path.join(result_path, url.rpartition('/')[2])) == False:
        try:
            respone = requests.get(url=url, headers=headers, allow_redirects=False)
            print('正在请求图片链接...', url)
            if respone.status_code == 302 or respone.status_code == 301:
                new_url = 'https://pixabay.com' + respone.headers['Location']
                new_respone = requests.get(url=new_url)
                if new_respone.status_code == 200:
                    write_img(new_respone, url, result_path)
        except Exception as e:
            print(e)
            print('图片下载失败')



def write_img(respone, url, result_path):
    with open(os.path.join(result_path, url.rpartition('/')[2]), 'wb') as fp:
        fp.write(respone.content)
        print('success', url)

if __name__ == '__main__':
    url_path = r'D:\scrapy_down\pixabay_face.txt'
    result_path = r'D:\scrapy_down\face'
    q = Queue()
    row_url = read_url(url_path, q)
    p = Pool(4)
    while True:
        if row_url.empty() == False:
            p.apply_async(downloads, args=(row_url.get(), result_path))
        else:
            break
    p.close()
    p.join()