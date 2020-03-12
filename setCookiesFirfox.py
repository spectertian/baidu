# coding=utf-8
from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

import time
import pickle
import json


def save_cookies(requests_cookiejar, filename):
    with open(filename, 'wb') as f:
        pickle.dump(requests_cookiejar, f, 0)


url = 'https://pan.baidu.com/s/1n890K1uMotIasOIwEQ5neQ'
tqm = '4cau'
tqmCssId = 'ktlJmA'
clickName = 'ivirlGXq'
cookies_file = '/Users/zhongsheng/test/baidu.cookies'
# driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Firefox(GeckoDriverManager().install())

# driver.get(url)
#
# cookies = pickle.load(open(cookies_file, "rb"))
# for cookie in cookies:
#     print(cookie)
#     if 'expiry' in cookie:
#         del cookie['expiry']
#     driver.add_cookie(cookie)
#
# driver.refresh()
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

# 开始登陆
time.sleep(5)
driver.find_element_by_id("TANGRAM__PSP_10__footerULoginBtn").click()

userName = '15611658186'
userPassword = '1986630tian168'
# userName = '18366189397'
# userPassword = 'baidu1001'
userNameCssId = 'TANGRAM__PSP_10__userName'
userPasswordCssId = 'TANGRAM__PSP_10__password'
submits = 'TANGRAM__PSP_10__submit'

driver.find_element_by_id(userNameCssId).send_keys(userName)
driver.find_element_by_id(userPasswordCssId).send_keys(userPassword)
driver.find_element_by_id(submits).click()

time.sleep(10)  # 等登录加载完成
cookies = driver.get_cookies()
print(cookies)
pickle.dump(driver.get_cookies(), open(cookies_file, "wb"))

# save_cookies(cookies, cookies_file)

# jsonCookies = json.dumps(cookies)
# # print(jsonCookies)
# with open(cookies_file, 'w') as f:
#     f.write(jsonCookies)

# save_cookies(cookies, cookies_file)

# 链接: https://pan.baidu.com/s/1lgSXM9s1XwLVtI3PTTKJSg 提取码: j5pj
