# -*- coding: utf-8 -*-
# Author: wkun
# Date: 2022-04-03 23:23:37
# Description:大麦网抢票

import os
import time
import pickle
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Concert():

    def __init__(self):
        self.status = 0
        self.login_status = 0
        self.damai_url = 'https://www.damai.cn/'  # 大麦网首页
        self.driver = self.get_driver()
        self.desired_capabilities = DesiredCapabilities.CHROME
        self.desired_capabilities["pageLoadStrategy"] = "none"

    def get_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--disable-blink-features=AutomationControlled')
        # options.add_argument('--headless')  # 无界面形式
        options.add_argument('--no-sandbox')  # 取消沙盒模式
        options.add_argument('--disable-setuid-sandbox')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--incognito')  # 启动进入隐身模式
        options.add_argument('--lang=zh-CN')  # 设置语言为简体中文
        options.add_argument('--user-agent=' + UserAgent().random)
        options.add_argument('--hide-scrollbars')
        options.add_argument('--disable-bundled-ppapi-flash')
        options.add_argument('--mute-audio')
        # options.add_argument('--proxy-server={}'.format(proxy(headers)))
        browser = webdriver.Chrome(options=options)
        browser.execute_cdp_cmd("Network.enable", {})
        browser.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
        with open('/home/wkun/dev/python/work/js/stealth.min.js') as f:
            js = f.read()
        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})
        browser.maximize_window()

        return browser

    # 打开登录界面，获取登录cookies
    def set_cookie(self):
        self.driver.get(self.damai_url)
        WebDriverWait(self.driver, 10).until(lambda x: x.find_element(By.XPATH, '//div[2]/div/div[3]/div[1]/div[1]/span'))
        self.driver.find_element(By.XPATH, '//div[2]/div/div[3]/div[1]/div[1]/span').click()  # 点击'登录'
        WebDriverWait(self.driver, 10).until(lambda x: x.find_element(By.XPATH, '//*[@id="login"]'))
        self.driver.find_element(by=By.XPATH, value='//*[@id="login-tabs"]/div[2]').click()
        self.driver.find_element(by=By.XPATH, value='//*[@id="login-tabs"]/div[3]').send_keys('18410065868')
        self.driver.find_element(by=By.XPATH, value='//*[@id="login-form"]/div[2]/div[3]/a').click()
        verification_code = input('请输入验证码：')
        self.driver.find_element(by=By.XPATH, value='//*[@id="fm-smscode"]').send_keys(verification_code)
        self.driver.find_element(by=By.XPATH, value='//*[@id="login-form"]/div[4]/button').click()
        a = self.driver.get_cookies()
        pickle.dump(a, open('cookies.pkl', 'wb'))
        print(a)


if __name__ == "__main__":
    Concert().set_cookie()
