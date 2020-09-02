import requests
from bs4 import BeautifulSoup
import random
def get_news(category):
  category_allowed = ['travel', 'sports', 'star', 'fashion', 'health', 'boba', 'speed', 'house', 'pets', 'game']
  if category not in category_allowed:
    return 404
  main_url = 'https://' + category + '.ettoday.net'
  res = requests.get(main_url)
  soup = BeautifulSoup(res.text, "html.parser")
  news_url = []
  for link in soup.find_all('a'):
    if link.get('href') == None:
      pass
    elif '/news/10' in link.get('href') and 'ettoday' not in link.get('href'):
      news_url.append(main_url + link.get('href'))
    elif category == 'travel' and '/article/10' in link.get('href') and 'https:' not in link.get('href'):
      news_url.append(main_url + link.get('href'))
    elif category == 'travel' and '/article/10' in link.get('href') and 'https:' in link.get('href'):
      news_url.append(link.get('href'))
    elif category == 'health' and '/news/10' in link.get('href') and 'https:' not in link.get('href'):
      news_url.append('https:' + link.get('href'))
    elif category == 'health' and '/news/10' in link.get('href') and 'https:' in link.get('href'):
      news_url.append(link.get('href'))
    elif category == 'boba' and '/videonews/' in link.get('href'):
      news_url.append(main_url + link.get('href'))
    elif category == 'speed' and '/news/10' in link.get('href') and 'https:' not in link.get('href'):
      news_url.append('https:' + link.get('href'))
    elif category == 'house' and '/news/10' in link.get('href'):
      news_url.append('https:' + link.get('href'))
    elif category == 'pets' and '/news/' in link.get('href'):
      news_url.append('https:' + link.get('href'))
    elif category == 'game' and '/article/' in link.get('href'):# and '/news/' in link.get('href'):
      news_url.append(main_url + link.get('href'))
  if len(news_url) != 0:
    target = news_url[int(random.random() * len(news_url))]
    return target
  else:
    return 404

def get_news_help():
  return '請輸入:看(旅遊、體育、星光、時尚、健康、播吧、車雲、房產、寵物、遊戲)新聞'