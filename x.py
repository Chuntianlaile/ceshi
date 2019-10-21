# File Name: /home/shiyanlou/code/requests_crawl.py

import requests
from bs4 import BeautifulSoup


# 使用 requests.get 方法发送请求，获取响应对象
r = requests.get('https://www.shiyanlou.com/courses')
# 创建 BeautifulSoup 类的实例
soup = BeautifulSoup(r.text, features='lxml')

# 创建空列表用于存储需要爬取的图片地址
url_list = []
# 将需要爬取的图片的地址存入列表
for div in soup.find_all('div', class_='col-sm-12 col-md-3'):
    url_list.append(div.img['src'])

# 爬取图片并存储到指定目录下
for url in url_list:
    r = requests.get(url)
    with open('pics/' + url.split('/')[-1], 'wb') as f:
        f.write(r.content)
