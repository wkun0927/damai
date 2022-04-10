#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: wkun
# Date: 2022-04-03 23:23:37
# Description:大麦网抢票

import os
import time
import pickle
from fake_useragent import UserAgent
from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Concert:

    def __init__(self):
        self.status = 0
        self.login_status = 0
        self.damai_url = 'https://www.damai.cn/'  # 大麦网首页
        self.driver = self.get_driver()

    def get_driver(self):
        # selenium反爬参数
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--disable-blink-features=AutomationControlled')
        prefs = {"profile.managed_default_content_settings.images": 2, "profile.managed_default_content_settings.javascript": 1, 'permissions.default.stylesheet': 2}
        options.add_experimental_option("prefs", prefs)  # 禁止图片、js、css加载
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
        desired_capabilities = DesiredCapabilities.CHROME  # 无需等待页面完全加载完成
        desired_capabilities["pageLoadStrategy"] = "none"
        # options.add_argument('--proxy-server={}'.format(proxy(headers)))
        browser = webdriver.Chrome(options=options, desired_capabilities=desired_capabilities)
        browser.execute_cdp_cmd("Network.enable", {})
        browser.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
        with open('/home/wkun/dev/python/work/js/stealth.min.js') as f:
            js = f.read()
        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})
        browser.maximize_window()

        return browser

    # 打开登录界面，获取登录cookies
    def save_cookie(self):
        self.driver.get(self.damai_url)
        WebDriverWait(self.driver, 10).until(lambda x: x.find_element(By.XPATH, '//div[2]/div/div[3]/div[1]/div[1]/span'))
        self.driver.find_element(By.XPATH, '//div[2]/div/div[3]/div[1]/div[1]/span').click()  # 点击'登录'
        print('###请扫码登录###')
        while True:
            if self.driver.title.find('大麦网-全球演出赛事官方购票平台-100%正品、先付先抢、在线选座！') != -1:
                break
        a = self.driver.get_cookies()
        pickle.dump(a, open('/home/wkun/dev/大麦网抢票/cookies.pkl', 'wb'))

    def set_cookie(self):
        try:
            cookies = pickle.load(open('/home/wkun/dev/大麦网抢票/cookies.pkl', 'rb'))  # 载入cookie
            for cookie in cookies:
                cookie_dict = {
                    'domain': '.damai.cn',  # 必须有，不然就是假登录
                    'name': cookie.get('name'),
                    'value': cookie.get('value'),
                    "expires": "",
                    'path': '/',
                    'httpOnly': False,
                    'HostOnly': False,
                    'Secure': False
                }
                self.driver.add_cookie(cookie_dict)
        except Exception as e:
            print(e)

    # 登录
    def login(self):
        pass

    def choose_ticket(self):
        pass


if __name__ == "__main__":
    Concert().save_cookie()
