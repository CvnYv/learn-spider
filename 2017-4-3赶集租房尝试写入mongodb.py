#! usr/bin/env python3
# -*- coding:utf-8 -*-


import requests
import re
import time
import pymongo
from bs4 import BeautifulSoup


# 连接数据库
client = pymongo.MongoClient('localhost', 12345)
ganjiZufang = client['ganjiZufang']
# 建立页面 需要爬取的url和商品详情页面
url_list = ganjiZufang['url_list']
items_info = ganjiZufang['items_info']
# 伪装浏览器
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.3'
                         '6 (KHTML, like Gecko) Ubuntu Chromium/56.0.2924.7'
                         '6 Chrome/56.0.2924.76 Safari/537.36'}


# 思路:先爬取房子url存储再逐个爬取详情
# 获取商品链接
def get_fang_url(page):
    count = 0
    for i in range(1, page + 1):
        url = 'http://cd.ganji.com/fang3/a1o%s/' % i
        html = requests.get(url, headers=headers).text
        puid = re.findall('id="puid-(.*?)"', html, re.S)
        # links = soup.select('div[class="f-list-item "]')  # 按原来思路出错的代码
        count += 1
        print('抓到第%s页链接' % count)
        for l in puid:
            fang_url = 'http://cd.ganji.com/fang3/%sx.htm' % l
            url_list.insert_one({'link': fang_url})
            print(fang_url)


# 获取商品详情
def get_items(url):
    zf_data = requests.get(url, headers=headers)
    if zf_data.status_code == 404:
        pass
    else:
        time.sleep(2)
        zf_data.encoding = 'utf-8'
        soup = BeautifulSoup(zf_data.text, 'lxml')
        data = {
            'title': soup.select(".card-title i")[0].get_text(strip=True),
            'price': soup.select(".price")[0].get_text(strip=True),
            'synopsis': soup.select(".fang-info")[0].get_text(" ", strip=True),
            'name': soup.select(".item-con")[0].get_text(strip=True),
            'area': soup.select(".item-con")[1].get_text(strip=True),
            'describe': soup.select(".describe")[0].get_text(strip=True),
            'url': url
        }
        print(data)
        items_info.insert_one(data)


def main():
    page = 63
    get_fang_url(page=page)
    it = url_list.find()
    for i in it:
        url = i['link']
        get_items(url=url)


if __name__ == '__main__':
    main()
