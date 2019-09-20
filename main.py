#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
from argparse import *

# urllib3.disable_warnings()

sys.path.insert(0, os.path.dirname(__file__))
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import UnexpectedAlertPresentException
import datetime
import json

def sendKeytoSoftKeyBoard(driver, key):
    key = key.upper()
    swith123 = driver.find_element(By.XPATH, "//a[@class='keyboard-key--switch keyboard-key--switch-to-panel123 fl']")
    swithabc = driver.find_element(By.XPATH, "//a[@class='keyboard-key--switch keyboard-key--switch-to-panelABC fl']")
    boardkey = driver.find_element(By.XPATH, "//a[@data-code='" + key + "']")
    # if not boardkey.is_displayed():
    #     print key
    #     if key.isdigit():
    #         swith123.click()
    #     else:
    #         swithabc.click()
    # boardkey.click()
    driver.execute_script("""
        var element = arguments[0];
        element.click()
        """, boardkey)

def sendPassword(driver, password):
    for x in xrange(0,len(password)):
        sendKeytoSoftKeyBoard(driver, password[x])

def __init__():
    if os.name == "posix":
        user_default_profile = os.path.join(os.path.expanduser('~'), ".config/google-chrome-test")
    elif os.name == "nt":
        user_default_profile = os.path.join(os.path.expanduser('~'), "AppData/Local/Google/Chrome/google-chrome-test")

    ChromeOptions = Options()
    ChromeOptions.add_argument("--user-data-dir=" + user_default_profile);
    browser = webdriver.Chrome(chrome_options=ChromeOptions)

    with open(os.path.join(os.path.dirname(__file__), "account.json")) as f:
        info = json.loads(f.read())
        passwd = info["passwd"]

    # Login Root url, save cookies, then click Files Button and get all tags
    browser.get("https://billcloud.unionpay.com/upwxs-rsmobile/inSports/wallet/detail?rightId=661&ticket=UCSSO-eX0MrEqaK2srvXAUIjxzAG2wNqyXKEJeizf&sysIdStr=HHfkqzIonmGC8RE&openId=6p0OXl3Whg7WcfI%2F8bFLmdmnAKEjsGmVUHyWkefGyDw%3D&token=_wGb15WL0kjZjJmM5MWZ1UGZtIDZmlTLkVjM00yYkhzMtYTN2gDZwEGM")
    book_button = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "button_1")))
    book_button.click()
    # input password
    pwd_input = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "pwdinput")))
    pwd_input.click()
    sendPassword(browser, passwd)
    captcha = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "captcha")))
    captcha.click()

    #In case of captcha wrong
    done = False
    while (not done):
        try:
            book_button = WebDriverWait(browser, 120).until(EC.presence_of_element_located((By.ID, "button_1")))
            done = True
        except UnexpectedAlertPresentException as e:
            browser.switch_to.alert.accept()

    book_button.click()
    next_button = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "nextPage")))
    next_button.click()
    agree_button = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "agreeBtn")))
    agree_button.click()
    ljyy_button = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "ljyy")))
    ljyy_button.click()
    confirm_Button = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//label[text()[contains(., '确认')]]")))
    confirm_Button.click()

    drag_button = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "wcse_drag_block")))
    actions = ActionChains(browser)
    actions.click_and_hold(drag_button).perform()
    # actions.release(drag_button).perform()
    # Below are available in 10:00
    # The confirm button will fade in 1 seconds, make buttons under it not clickable.
    # So after click it, just delete the whole <div> section and then go on
    confirm_Button = WebDriverWait(browser, 1200).until(EC.presence_of_element_located((By.XPATH, "//div[text()[contains(., '确定')]]")))
    confirm_Button.click()
    browser.execute_script("""
        var element = arguments[0];
        element.parentNode.parentNode.parentNode.parentNode.removeChild(element.parentNode.parentNode.parentNode)
        """, confirm_Button)

    hotel_name = WebDriverWait(browser, 1200).until(EC.element_to_be_clickable((By.XPATH, "//h2[text()[contains(., '华尔道夫')]]/../..")))
    hotel_name.click()

    today = datetime.date.today()
    next_sunday = (today + datetime.timedelta(((6-today.weekday()) % 7) if today.weekday() < 6 else 7 )).strftime('%m-%d')

    date_name = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.ID, "date")))
    date_name.click()
    select_date_name = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//span[@data-value='" + next_sunday + "']")))
    current_date_name = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//span[@data-value='" + next_sunday + "']/.."))).find_element(By.XPATH, "//span[@class='on']")
    browser.execute_script("arguments[0].setAttribute('class', '')", current_date_name)
    browser.execute_script("arguments[0].setAttribute('class', 'on')", select_date_name)
    confirm_Button = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='sure']")))
    confirm_Button.click()
    confirm_Button = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//a[@class='venuesBookBtn boxflex font18']")))
    confirm_Button.click()

    confirm_Button = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//a[@class='x_tjdd_btns font17']")))
    confirm_Button.click()

    pay_Button = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//button[text()[contains(., '支付')]]")))
    pay_Button.click()


    # try:
    #     passwd_input = WebDriverWait(browser, self.DEFAULT_TIME_OUT).until(EC.presence_of_element_located((By.NAME, "PASSWORD_INPUT")))
    #     log_in = WebDriverWait(browser, self.DEFAULT_TIME_OUT).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
    #     user_input.send_keys(self.account)
    #     passwd_input.send_keys(self.passwd)
    #     log_in.click()
    # except:
    #     browser.quit()
    #     raise

    # try:
    #     Files_Button = WebDriverWait(browser, self.DEFAULT_TIME_OUT).until(EC.presence_of_element_located((By.XPATH, "//a[text()[contains(., 'Files')]]")))
    # except:
    #     try:
    #         confirm = WebDriverWait(browser, self.DEFAULT_TIME_OUT).until(EC.presence_of_element_located((By.XPATH, "//input[@name='_action_cont']")))
    #         confirm.click()
    #         Files_Button = WebDriverWait(browser, self.DEFAULT_TIME_OUT).until(EC.presence_of_element_located((By.XPATH, "//a[text()[contains(., 'Files')]]")))
    #     except:
    #         browser.quit()
    #         raise

    # https://shzs.bestdo.com/orders/golfpractice/createOrder?mer_item_id=10210491000109&mer_id=1021049&book_day=2019-09-21&hours=06:00-23:00
    # https://billcloud.unionpay.com/upwxs-rsmobile/bestdo/wallet/payFront
    # https://shzs.bestdo.com/orders/golfpractice/createOrder?mer_item_id=10210491000113&mer_id=1021049&book_day=2019-09-21&hours=09:00-22:00
    # https://shzs.bestdo.com/mer/item/info?cid=121&mer_item_id=10210491000113
    # https://shzs.bestdo.com/mer/lists?mer_id=1021049&mer_price_id=4224&cid=121&city=52

__init__()
while True:
  pass