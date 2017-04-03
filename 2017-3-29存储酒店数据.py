#! usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
import csv
from bs4 import BeautifulSoup


def parse_html(writer):
    for n in range(1, 51):
        url = 'http://www.dianping.com/chengdu/hotel/p' + str(n)
        html = requests.get(url, headers={
            'user-Agent': 'Mozilla/5.0 (X11; Linux x86_64) Apple'
                          'WebKit/537.36 (KHTML, like Gecko) '
                          'Ubuntu Chromium/56.0.2924.76 '
                          'Chrome/56.0.2924.76 Safari/537.36'
        }).content
        soup = BeautifulSoup(html, "lxml")
        ul_list = soup.find("ul", attrs={"class": "hotelshop-list"})
        for li_list in ul_list.find_all("li", attrs={"class": " hotel-block"
                                                     " J_hotel-block"}):
            hotel_name = li_list.find("h2", attrs={"class": "hotel-name"}).a.string
            hotel_url = 'http://www.dianping.com' + li_list.find("h2", attrs={
                "class": "hotel-name"}).a['href']
            hotel_place = li_list.find("p", attrs={"class": "place"}).a.string\
                          + ', ' + li_list.find("span", attrs={"class": "walk-dist"}).string
            hotel_price = li_list.find("div", attrs={"class": "price"}).strong.string
            writer.writerow((hotel_name, hotel_place, hotel_price, hotel_url))

        print("抓到第%d页" % n)


def main():
    csv_file = open("../files/chengduhotel.csv", 'wt', encoding='utf-8')
    try:
        writer = csv.writer(csv_file)
        writer.writerow(('酒店名称', '位置', '价格', '详情链接'))
        parse_html(writer)
    finally:
        csv_file.close()


if __name__ == '__main__':
    main()




# 框架风格
# DOWNLOAD_URL = 'http://www.dianping.com/tianjin/hotel'


# def download_page(url):
#     return requests.get(url, headers={
#         'user-Agent': 'Mozilla/5.0 (X11; Linux x86_64) Apple'
#                       'WebKit/537.36 (KHTML, like Gecko) '
#                       'Ubuntu Chromium/56.0.2924.76 '
#                       'Chrome/56.0.2924.76 Safari/537.36'
#     }).content

