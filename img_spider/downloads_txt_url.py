import requests
import os


row_url = []
with open("url.txt", 'r', encoding='utf-8') as file:
    for line in file.readlines():
        if line[-1] == "\n":
            row_url.append(line[0:-1])
        else:
            row_url.append(line)

headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        }
row_url = list(set(row_url))
for url in row_url:
    print(url)
    try:
        res = requests.get(url=url, headers=headers)
        print('正在请求图片链接...', url)
        if res.status_code == 200:
            with open(os.path.join(r'D:\work', url.rpartition('/')[2]), 'wb') as fp:
                fp.write(res.content)
    except Exception as e:
        print(e)
        print('图片下载失败')

    # with open(os.path.join(r'D:\work', 'test.txt'), 'a') as fp:
    #     fp.write(str(url))
    #     fp.write('\n')








