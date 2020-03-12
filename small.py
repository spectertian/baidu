# coding=utf-8
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from aip import AipOcr
import requests
import base64
import urllib.request
import os

import pytesseract
from PIL import Image

client = AipOcr('18671664', 'O0d2Tgv4imtAfVqhQF49py0o', 'au1xuxZlqqROnOjlVqLCfHhO4lLQZICl')

import json
import time
import pickle
import urllib.parse
import re
# import nal



# print(html)
# exit('zss')

# 开启performance日志记录
# chrome_options = Options()


def save_cookies(requests_cookiejar, filename):
    with open(filename, 'wb') as f:
        pickle.dump(requests_cookiejar, f, 0)

#链接: https://pan.baidu.com/s/1nrCL8vY61aKApKhrkwJd9A 提取码: gbq7 复制这段内容后打开百度网盘手机App，操作更方便哦
url = 'https://pan.baidu.com/s/1nrCL8vY61aKApKhrkwJd9A'
tqm = 'gbq7'
tqmCssId = 'ktlJmA'
clickName = 'ivirlGXq'
cookies_file = '/Users/zhongsheng/test/baidu.cookies'

urlArr = url.rsplit('/', 1)
downloadUrl = '/Users/zhongsheng/PycharmProjects/baidu2/' + urlArr[1]
print(downloadUrl)
# exit()

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory": downloadUrl}
chromeOptions.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chromeOptions)

# driver = webdriver.Chrome(executable_path="C:\python\chromedriver.exe", chrome_options=chrome_options,
#                           desired_capabilities=caps)
# driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options, desired_capabilities=caps)
# driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
# driver = webdriver.Firefox(executable_path='/Users/zhongsheng/test/geckodriver')
# driver = webdriver.Firefox()


driver.get(url)

cookies = pickle.load(open(cookies_file, "rb"))
for cookie in cookies:
    # print(cookie)
    if 'expiry' in cookie:
        del cookie['expiry']
    driver.add_cookie(cookie)

# driver.refresh()
# time.sleep(4)
driver.get(url)

# info = driver.find_element_by_xpath("//a[@node-type='header-login-btn']").text
# print(info);
# if info == '登录':
# elem = driver.find_element_by_id(tqmCssId)
# elem.send_keys(tqm)
# element = driver.find_element_by_id(clickName)
# driver.execute_script("arguments[0].click();", element)

# 下载页面
time.sleep(5)
driver.find_element_by_xpath("//a[@data-button-id='b3']").click()
# # print(jsonCookies)
# with open(cookies_file, 'w') as f:
#     f.write(jsonCookies)

# save_cookies(cookies, cookies_file)

# 链接: https://pan.baidu.com/s/1lgSXM9s1XwLVtI3PTTKJSg 提取码: j5pj
# js事件执行发送请求后浏览器弹窗下载，拿到日志记录


time.sleep(10)


for a in range(100):
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

    driver.find_element_by_link_text('换一张').click()




def every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.execute_script('window.open()')
        # 定位到新的页面
        driver.switch_to_window(driver.window_handles[1])
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = downloads.Manager.get().items_;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.file_url);
        """)


# waits for all the files to be completed and returns the paths
paths = WebDriverWait(driver, 120, 1).until(every_downloads_chrome)

print(paths)
time.sleep(10)
driver.quit()
exit()






def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


options = {}
options["language_type"] = "CHN_ENG"
options["detect_direction"] = "true"
options["detect_language"] = "true"
options["probability"] = "true"
yzm = ''
for a in range(100):
    img = driver.find_element_by_xpath("//img[@class='img-code']").get_attribute('src')
    urllib.request.urlretrieve(img, '3.jpeg')

    # strs = client.basicGeneralUrl(img, options)

    image = get_file_content('3.jpeg')

    strs = client.basicGeneral(image, options)
    print(img)
    print(strs)

    if strs['words_result']:
        yzm = strs['words_result'][0]['words']
        print(strs['words_result'][0])
        # print(strs['words_result']['words'])
    # driver.find_element_by_xpath("//span[@class='text']").click()
    time.sleep(1)
    elemYzm = driver.find_element_by_xpath("//input[@class='input-code']")
    elemYzm.send_keys('')
    elemYzm.send_keys(yzm)

    time.sleep(1)
    print('#############点击')
    driver.find_element_by_xpath("//a[@class='underline']").click()
    elemYzm.send_keys('')

    print(a)
    print('#############')
    time.sleep(1)

# browser_log = driver.get_log('performance')
# browser_log.reverse()
# print(browser_log)
# for i in browser_log:
#     if i.get('message'):
#         message_dict = json.loads(i.get('message'))
#         file_download_url = message_dict.get('message').get('params').get('url') if message_dict else None
#
# print(file_download_url)
