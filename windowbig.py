# coding=utf-8
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import time
import pickle
import base64
import urllib.request
import urllib.parse
import json
import re

# 保存cookies
def save_cookies(requests_cookiejar, filename):
    with open(filename, 'wb') as f:
        pickle.dump(requests_cookiejar, f, 0)
# 链接:https://pan.baidu.com/s/1-EDGBSx4c8SNt4o_aeuJ6Q  密码:62s9
# 链接:https://pan.baidu.com/s/1R-8Rk-ffh5H9HZ7xtv8ESw  密码:dkqg

url = 'https://pan.baidu.com/s/1wXE1tFsl2lI18lylB6I_bQ'
tqm = 'nvwx'
# tqm = 'cyev'
tqmCssId = 'ktlJmA'
clickName = 'ivirlGXq'
cookies_file = 'baidu.cookies'
driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(url)

cookies = pickle.load(open(cookies_file, "rb"))
for cookie in cookies:
    print(cookie)
    if 'expiry' in cookie:
        del cookie['expiry']
    driver.add_cookie(cookie)

driver.refresh()
driver.get(url)
time.sleep(3)

# info = driver.find_element_by_xpath("//a[@node-type='header-login-btn']").text
# print(info);
# if info == '登录':
elem = driver.find_element_by_id(tqmCssId)
elem.send_keys(tqm)
element = driver.find_element_by_id(clickName)
driver.execute_script("arguments[0].click();", element)

# 下载页面
time.sleep(5)
driver.find_element_by_xpath("//a[@data-button-id='b3']").click()
time.sleep(5)


for a in range(100):
    driver.find_element_by_link_text('换一张').click()

    time.sleep(2)
    img = driver.find_element_by_xpath("//img[@class='img-code']").get_attribute('src')
    urllib.request.urlretrieve(img, '23.jpeg')
    # exit('aa')
    time.sleep(2)
    # encodestr = nal.getImg('23.jpeg')
    # dict = {'img': encodestr}
    # yzm = nal.getYzm(dict)
    # print(yzm)

    # API产品路径
    host = 'https://codevirify.market.alicloudapi.com'
    path = '/icredit_ai_image/verify_code/v1'
    # 阿里云APPCODE
    appcode = '712d406485a44077a7e72d7b03a2af36'
    bodys = {}
    url = host + path

    # 内容数据类型，如：0，则表示BASE64编码；1，则表示图像文件URL链接

    # 启用BASE64编码方式进行识别
    # 内容数据类型是BASE64编码
    # f = open(r'23.jpeg', 'rb')
    # contents = base64.b64encode(f.read())
    # f.close()
    with open('23.jpeg', 'rb') as f:  # 以二进制读取本地图片
        data = f.read()
        contents = str(base64.b64encode(data), 'utf-8')
    bodys['IMAGE'] = contents
    bodys['IMAGE_TYPE'] = '0'

    # 启用URL方式进行识别
    # 内容数据类型是图像文件URL链接
    # bodys['IMAGE'] = '图片URL链接'
    # bodys['IMAGE_TYPE'] = '1'

    post_data = urllib.parse.urlencode(bodys).encode('utf-8')
    request = urllib.request.Request(url, post_data)
    request.add_header('Authorization', 'APPCODE ' + appcode)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    response = urllib.request.urlopen(request)
    content = response.read()
    yzm = ''
    if (content):
        print(content.decode('utf-8'))
        ss = content.decode("utf8")
        print(ss)

        ss1 = json.loads(ss)
        aa = ss1['VERIFY_CODE_ENTITY']['VERIFY_CODE']
        # aa = ss1['prism_wordsInfo'][0]['word']
        yzm = re.sub('\s', '', aa)

        # print(strs['words_result']['words'])
    # driver.find_element_by_xpath("//span[@class='text']").click()
    time.sleep(1)
    elemYzm = driver.find_element_by_xpath("//input[@class='input-code']")
    elemYzm.clear()
    elemYzm.send_keys(yzm)

    time.sleep(1)
    print('#############点击')
    # driver.find_element_by_xpath("//a[@class='underline']").click()
    driver.find_element_by_link_text('确定').click()

    print('#############')
    time.sleep(2)




# obj = driver.switch_to.alert
# time.sleep(2)
# obj.accept()
dialog_box = driver.switch_to.alert
# dialog_box = driver.switch_to_alert()
'''添加等待时间'''
time.sleep(2)
'''获取对话框的内容'''
#打印警告对话框内容
print (dialog_box.text)
'''点击【确认】显示"您为何如此？"'''
dialog_box.accept()   #接受弹窗


# 开始登陆
# time.sleep(2)
# driver.find_element_by_id("TANGRAM__PSP_10__footerULoginBtn").click()

# userName = '15611658186'
# userPassword = '1986630tian168'
# # userName = '18366189397'
# # userPassword = 'baidu1001'
# userNameCssId = 'TANGRAM__PSP_10__userName'
# userPasswordCssId = 'TANGRAM__PSP_10__password'
# submits = 'TANGRAM__PSP_10__submit'
#
# driver.find_element_by_id(userNameCssId).send_keys(userName)
# driver.find_element_by_id(userPasswordCssId).send_keys(userPassword)
# driver.find_element_by_id(submits).click()

# time.sleep(10)  # 等登录加载完成
# cookies = driver.get_cookies()
# print(cookies)
# pickle.dump(driver.get_cookies(), open(cookies_file, "wb"))

# save_cookies(cookies, cookies_file)

# jsonCookies = json.dumps(cookies)
# # print(jsonCookies)
# with open(cookies_file, 'w') as f:
#     f.write(jsonCookies)

# save_cookies(cookies, cookies_file)

# 链接: https://pan.baidu.com/s/1lgSXM9s1XwLVtI3PTTKJSg 提取码: j5pj
