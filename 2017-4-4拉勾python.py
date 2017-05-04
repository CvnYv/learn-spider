#! usr/bin/env python3
# -*- coding:utf-8 -*-


import requests
import json
import time
import pymongo


# 连接数据库
client = pymongo.MongoClient('127.0.0.1', 12345)
lagou = client['lagou']
job_detail = lagou['job_detail']


# 学用类定义爬虫
class Spider():
    def __init__(self):
        self.keyword = input('请输入职位: ')

    # 抓取数据
    def get_data(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/5'
                                 '37.36 (KHTML, like Gecko) Ubuntu Chromium/56.'
                                 '0.2924.76 Chrome/56.0.2924.76 Safari/537.36',
                   'cookie': 'user_trace_token=20161129111754-1f0acc024f0c42f5'
                             '8c1eda2a9716e9e3; LGUID=20161129111754-6b0b0d3d-'
                             'b5e2-11e6-9de0-525400f775ce; JSESSIONID=A3AD62F6'
                             '7A40D6EE863DCC38A38A4250; _putrc=C58E73D8FD50161'
                             '8; login=true; unick=%E7%8E%8B%E9%9B%85%E5%8D%9A'
                             '; showExpriedIndex=1; showExpriedCompanyHome=1; '
                             'showExpriedMyPublish=1; hasDeliver=0; TG-TRACK-C'
                             'ODE=search_code; SEARCH_ID=3d6bea808cac4df1a9b36'
                             'b209a300420; index_location_city=%E6%88%90%E9%83'
                             '%BD; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=148'
                             '9368817,1489636441,1491107739,1491311886; Hm_lpv'
                             't_4233e74dff0ae5bd0a3d81c6ccf756e6=1491316646; _'
                             'ga=GA1.2.527162507.1480389474; LGSID=20170404215'
                             '840-cefc488c-193e-11e7-8d3b-525400f775ce; LGRID='
                             '20170404223726-38fe36a5-1944-11e7-989c-5254005c3'
                             '644'
                   }
        html = requests.get(url, headers=headers)
        data = json.loads(html.text)
        return data

    # 构建url
    def save_detail(self):
        self.New = int(input('请输入要爬取的页数:'))
        self.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print('本地时间: '+self.time)
        print('开始采集数据...')
        for page in range(1, self.New+1):
            self.url = 'https://www.lagou.com/jobs/positionAjax.json?px=new&' \
                       'first=true&pn=' + str(page) + '&kd=' + str(self.keyword)
            time.sleep(3)
            self.get_position()
            print('第%s项录入完毕' % page)

    # 获取职位信息存入mongodb
    def get_position(self):
        data = self.get_data(url=self.url)
        position = data['content']['positionResult']['result']
        if position is not None:
            for i in position:
                detail = {
                    'companyFullName': i['companyFullName'],
                    'city': i['city'],
                    'companyId': i['companyId'],
                    'companyLabelList': i['companyLabelList'],
                    'companySize': i['companySize'],
                    'createTime': i['createTime'],
                    'district': i['district'],
                    'education': i['education'],
                    'financeStage': i['financeStage'],
                    'jobNature': i['jobNature'],
                    'positionAdvantage': i['positionAdvantage'],
                    'positionId': i['positionId'],
                    'positionName': i['positionName'],
                    'publisherId': i['publisherId'],
                    'salary': i['salary'],
                    'secondType': i['secondType'],
                    'workYear': i['workYear']
                }
                # print(detail)
                job_detail.insert_one(detail)


spider = Spider()
spider.save_detail()