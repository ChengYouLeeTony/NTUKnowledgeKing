import requests
from bs4 import BeautifulSoup
import urllib
from selenium import webdriver

def translate_ch_en(query):
  code = urllib.parse.quote(query)
  driver = webdriver.PhantomJS(executable_path='./bin/phantomjs')  # PhantomJs
  driver.get('https://translate.google.com.tw/?hl=zh-TW#zh-CN/en/' + code)  # 輸入範例網址，交給瀏覽器
  pageSource = driver.page_source  # 取得網頁原始碼
  driver.close()  # 關閉瀏覽器
  soup = BeautifulSoup(pageSource, "html.parser")
  for link in soup.find_all(id='result_box'):
    result = str(link.span.contents[0])
  return result

def translate_en_ch(query):
  code = urllib.parse.quote(query)
  driver = webdriver.PhantomJS(executable_path='./bin/phantomjs')  # PhantomJs
  driver.get('https://translate.google.com.tw/?hl=zh-TW#en/zh-TW/' + code)  # 輸入範例網址，交給瀏覽器
  pageSource = driver.page_source  # 取得網頁原始碼
  soup = BeautifulSoup(pageSource, "html.parser")
  for link in soup.find_all(id='result_box'):
    result = str(link.span.contents[0])
  return result