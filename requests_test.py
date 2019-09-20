# import requests
# import json
# import os
# import re
#
# url = 'https://www.ximalaya.com/revision/play/album?albumId=19492295&pageNum=2&sort=1&pageSize=30'
#
# # headers = {
# #             'Accept': "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
# #             'Accept-Language': "en-US,en;q=0.9",
# #             'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
# #             'cookie': '__cfduid = d9efff7c4dd6d4336a55290f505e5ae211568683206;_ga = GA1.2.1646761631.1568683208;_gid = GA1.2.464847544.1568683208;is_human = 1;lang = zh;csrftoken = edxF4q8bBb3oAoItPNX4ZFDRAVwRBjEnczM5bxmVie514LjXYWVSx9etGHAlPueR;sessionid = ".eJxVjEsOgyAUAO_CujGK8qC9DHngq9ACNnw2Nr17rYsmbicz82Y6YFoaLsRubHPswjS26nQrlLXD4nYMCtUdJyFm1Q9yNKiMGAAEgQSQiksCCz3xc2zQPinNe__K64Ns7Vr1oXS2lbrGQ-z8oSaMpNesKaIP_-4087_PMMJ0HXvOPl-VKT0l:1iA2Pg:YhbVSZ_qtIrQZMm5ai3P6Atf6V4";client_width = 1208'
# #
# #         }
# # respone = requests.get(url=url, headers=headers, allow_redirects=False)
# # print(respone)
# # print(respone.status_code)
# # print(respone.headers['Location'])
# # new_url = 'https://pixabay.com' + respone.headers['Location']
# #
# # new_respone = requests.get(url=new_url)
# # with open(os.path.join(r'D:\scrapy_down', '0001.jpg'), 'wb') as fp:
# #     fp.write(new_respone.content)
#
#
#
# headers = {
#             'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
# }
# respone = requests.get(url=url, headers=headers)
# print(respone.text)
# # d = json.loads(respone.text)
# # print(d)
# # pattern = re.compile('"url": "(.*?)","fileSizeInBytes"')
# # img_list = re.findall(pattern, respone.text)
# # print(img_list)

