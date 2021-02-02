# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 08:28:37 2021

@author: kevin
"""


from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import time

def crawl(hashtag):
    
    browser = webdriver.Chrome('./chromedriver')
    url = 'https://www.instagram.com/'  
    
    # ------ 前往該網址 ------
    browser.get(url) 
    
    # ------ 填入帳號與密碼 ------
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.NAME, 'username')))
    
    # ------ 網頁元素定位 ------
    username_input = browser.find_elements_by_name('username')[0]
    password_input = browser.find_elements_by_name('password')[0]
    print("inputing username and password...")
    
    # ------ 輸入帳號密碼 ------
    username_input.send_keys("iim3chatbot")
    password_input.send_keys("imchatbot!")
    
    # ------ 登入 ------
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH,
    '//*[@id="loginForm"]/div/div[3]/button/div')))
    # ------ 網頁元素定位 ------
    login_click = browser.find_elements_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div')[0]
    # ------ 點擊登入鍵 ------
    login_click.click()
    
    
    
    # ------ 不儲存登入資料 ------
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button')))
    
    # ------網頁元素定位 ------
    store_click = browser.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')[0]
    
    # ------ 點擊不儲存鍵 ------
    store_click.click()
    
    
    # ------ 不開啟通知 ------
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div/div[3]/button[2]')))
    
    # ------ 網頁元素定位 ------                                                                                                    
    notification_click = browser.find_elements_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')[0]
    
    # ------ 點擊不開啟通知 ------
    notification_click.click()
    print('Log in ')
    
    # 往下滑並取得新的貼文連結
 
    #將地點去除一些很奇怪的符號 因為ig tag搜尋不能有這些符號
    hashtag = hashtag.split("_")[0].split(' ')[0].split('-')[0].split('/')[0]

    url = 'https://www.instagram.com/explore/tags/'+hashtag
    browser.get(url) # 前往該網址
    #print("等待")
    time.sleep(2)
    #print("好了")
    #n_scroll = 1
    post_url = []
    img_url = []
    #for i in range(n_scroll):
    #scroll = 'window.scrollTo(0, document.body.scrollHeight);'
    #browser.execute_script(scroll)
    html = browser.page_source
    #print("等待")
    time.sleep(2)
    #print("好了")
    soup = BeautifulSoup(html, 'html.parser')

    # 尋找所有的貼文連結
    
    #obj = soup.find_all('a',class_="v1Nh3 kIKUG  _bz0w")
    obj = soup.select('article div div div div a')
    #print(obj)
    for elem in obj:
        # 如果新獲得的貼文連結不在列表裡，則加入
        if len(post_url)<9:
            #if elem['href'] not in post_url:
            post_url.append('https://www.instagram.com/'+ elem['href'])
            img_url.append(elem.find('img').get('src'))

        #time.sleep(2) # 等待網頁加載
    
    post_img_list = []
    for a in range(len(post_url)):
        post_img_list.append([post_url[a],img_url[a]])
        
    # 總共加載的貼文連結數
    #print("總共取得 " + str(len(post_url)) + " 篇熱門貼文連結")
    #print(post_img_list)
    return(post_img_list)
    
#post_url_list = crawl('iim3chatbot', 'imchatbot!')










