from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


driver = webdriver.Chrome()
# cookie = {'cookie': '__cfduid = d9efff7c4dd6d4336a55290f505e5ae211568683206;_ga = GA1.2.1646761631.1568683208;_gid = GA1.2.464847544.1568683208;is_human = 1;lang = zh;csrftoken = edxF4q8bBb3oAoItPNX4ZFDRAVwRBjEnczM5bxmVie514LjXYWVSx9etGHAlPueR;sessionid = ".eJxVjEsOgyAUAO_CujGK8qC9DHngq9ACNnw2Nr17rYsmbicz82Y6YFoaLsRubHPswjS26nQrlLXD4nYMCtUdJyFm1Q9yNKiMGAAEgQSQiksCCz3xc2zQPinNe__K64Ns7Vr1oXS2lbrGQ-z8oSaMpNesKaIP_-4087_PMMJ0HXvOPl-VKT0l:1iA2Pg:YhbVSZ_qtIrQZMm5ai3P6Atf6V4";client_width = 1208'}
# driver.add_cookie(cookie)
driver.get("https://yandex.com/images/search?text=face&from=tabbar&p=1")
driver.get("https://yandex.com/images/search?text=face&from=tabbar&p=2")
# time.sleep(10)
# driver.quit()



