# coding=utf-8
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time
import pickle
import urllib.request
import urllib.parse
import base64
import json
import re

import sys
import getopt

tqm = url = task_id = ""


def inputArg(argv):
    global tqm, url, task_id

    try:
        opts, args = getopt.getopt(argv, "ht:u:i:", ["help", "tqm=", "url=", "task_id="])
    except getopt.GetoptError:
        print('Erro baidu_download.py -t <tqm> -u <url> -i <task_id>')
        print('or baidu_download.py --tqm=<tqm> --url=<url> --task_id=<task_id>')
        sys.exit(2)

    # 处理 返回值options是以元组为元素的列表。
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('baidu_download.py -t <tqm> -u <url> -i <task_id>')
            print('or baidu_download.py --tqm=<tqm> --url=<url> --task_id=<task_id>')
            sys.exit()
        elif opt in ('-t', '--tqm'):
            tqm = arg
        elif opt in ('-u', '--url'):
            url = arg
        elif opt in ('-i', '--task_id'):
            task_id = arg


inputArg(sys.argv[1:])

print('url为：', url)
print('tqm为：', tqm)
print('task_id为：', task_id)


# exit()
# python baidu_download.py -u https://pan.baidu.com/share/init?surl=QNooYs0oK57sO3qZmoVjRw  -t f06r -i 1323
#链接: https://pan.baidu.com/s/1KxdveBv3Rza7Yhw178K27g 提取码: xjsw 复制这段内容后打开百度网盘手机App，操作更方便哦
# python baidu_download.py -u https://pan.baidu.com/s/1KxdveBv3Rza7Yhw178K27g   -t xjsw -i 1323

def save_cookies(requests_cookiejar, filename):
    with open(filename, 'wb') as f:
        pickle.dump(requests_cookiejar, f, 0)


def isElementExist(css):
    try:
        driver.find_element_by_css_selector(css)
        return True
    except:
        return False


def isElementExistByXPath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False


tqmCssId = 'ktlJmA'
clickName = 'ivirlGXq'
# cookies 文件保存地址
cookies_file = '/Users/zhongsheng/test/baidu.cookies'

# 创建下载目录
urlArr = url.rsplit('/', 1)
downloadUrl = './download/' + urlArr[1]
chromeOptions = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, "download.default_directory": downloadUrl}
chromeOptions.add_experimental_option("prefs", prefs)
# 初始化浏览器
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chromeOptions)

driver.get(url)

# ##写入cookies
# cookies = pickle.load(open(cookies_file, "rb"))
# for cookie in cookies:
#     print(cookie)
#     if 'expiry' in cookie:
#         del cookie['expiry']
#     driver.add_cookie(cookie)

## 页面刷新授权
# driver.refresh()
# driver.get(url)

try:
    element = WebDriverWait(driver, 2).until(
        # EC.presence_of_element_located((By.ID, 'xxxx'))
        EC.presence_of_element_located((By.ID, tqmCssId))
    )
except ValueError:
    driver.quit()
# info = driver.find_element_by_xpath("//a[@node-type='header-login-btn']").text
# print(info);
# if info == '登录':

## 输入验证码跳转到 下载页面
elem = driver.find_element_by_id(tqmCssId)
elem.send_keys(tqm)
elements = driver.find_element_by_id(clickName)
driver.execute_script("arguments[0].click();", elements)
driver.refresh()


# 跳转页面等待
try:
    element = WebDriverWait(driver, 10).until(
        # EC.presence_of_element_located((By.ID, 'xxxx'))
        EC.presence_of_element_located((By.XPATH, "//a[@data-button-id='b3']"))
    )
except ValueError:
    driver.quit()


##写入cookies
cookies = pickle.load(open(cookies_file, "rb"))
for cookie in cookies:
    print(cookie)
    if 'expiry' in cookie:
        del cookie['expiry']
    driver.add_cookie(cookie)


# 判断是不是多选文件
time.sleep(1)
hasCheckAll = isElementExistByXPath("//div[@node-type='fydGNC']")
if hasCheckAll is True:
    driver.find_element_by_xpath("//div[@node-type='fydGNC']").click()

time.sleep(1)

# 点击下载文件
driver.find_element_by_xpath("//a[@data-button-id='b3']").click()

## 是否是需要输入验证码
time.sleep(2)
isYzm = isElementExistByXPath("//img[@class='img-code']")

if isYzm is True:
    for a in range(100):
        time.sleep(2)
        try:
            elemYzm = driver.find_element_by_xpath("//input[@class='input-code']")
            elemYzm.clear()
        except Exception as e:
            print("已经验证成功")
            break
        img = driver.find_element_by_xpath("//img[@class='img-code']").get_attribute('src')
        urllib.request.urlretrieve(img, '23.jpeg')
        time.sleep(2)
        # API产品路径
        host = 'https://codevirify.market.alicloudapi.com'
        path = '/icredit_ai_image/verify_code/v1'
        # 阿里云APPCODE
        appcode = '712d406485a44077a7e72d7b03a2af36'
        bodys = {}
        url = host + path
        with open('23.jpeg', 'rb') as f:  # 以二进制读取本地图片
            data = f.read()
            contents = str(base64.b64encode(data), 'utf-8')
        bodys['IMAGE'] = contents
        bodys['IMAGE_TYPE'] = '0'

        post_data = urllib.parse.urlencode(bodys).encode('utf-8')
        request = urllib.request.Request(url, post_data)
        request.add_header('Authorization', 'APPCODE ' + appcode)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
        response = urllib.request.urlopen(request)
        content = response.read()
        yzm = ''
        if (content):
            print(content.decode('utf-8'))
            result = content.decode("utf8")
            res = json.loads(result)
            res1 = res['VERIFY_CODE_ENTITY']['VERIFY_CODE']
            yzm = re.sub('\s', '', res1)
        time.sleep(1)
        elemYzm = driver.find_element_by_xpath("//input[@class='input-code']")
        elemYzm.clear()
        elemYzm.send_keys(yzm)

        time.sleep(1)
        print('#############点击')
        driver.find_element_by_link_text('确定').click()
        print('#############')
        time.sleep(1)

time.sleep(2)

try:
    dialog_box = driver.switch_to.alert
    print(dialog_box.text)
    ## 接受弹窗
    dialog_box.accept()
except Exception as e:
    print("不需要确定")

time.sleep(5)
print('退出')
driver.quit()
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
