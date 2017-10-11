# -*- coding: UTF-8 -*-

import re
import time
from pprint import pprint

import pandas as pd
import requests


class Snowball:
    xq = 'https://xueqiu.com'
    # 雪球自选股列表相关json
    url = {'get': xq + '/v4/stock/portfolio/stocks.json',
           'del': xq + '/stock/portfolio/delstock.json',
           'add': xq + '/v4/stock/portfolio/addstock.json',
           'modify': xq + '/v4/stock/portfolio/modifystocks.json'}
    # 默认cookie
    df_cookie = ('s=f71gpk9q7h; '
                 'xq_a_token=ed965d6ca0f68aa2f0b4a80a510e86fe5c02784d; '
                 'xq_r_token=fdcc8cfbe737cc4ba5146adb235fd757dc4acc3f; '
                 )

    def __init__(self, uid, cookie=df_cookie):
        self.uid = uid  # 用户页面如 https://xueqiu.com/6490571482
        self.cookie = cookie  # 操作列表需要该用户登录的cookie
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) '
                                      'Gecko/20100101 Firefox/56.0',
                        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Referer': Snowball.xq + '/' + uid,
                        'Cookie': cookie,
                        'DNT': '1'}
        self.stocks = pd.DataFrame()  # 雪球自选股清单

    def get_stocks(self):
        # 获取雪球自选股列表
        try:
            payload = {'size': 1000, 'tuid': self.uid, 'uid': self.uid, 'pid': -1, 'category': 2, 'type': 1}
            response = requests.get(Snowball.url['get'], params=payload, headers=self.headers, timeout=10)
            # pprint(response.content)
            self.stocks = pd.DataFrame(response.json()['stocks'])
        except Exception, e:
            print 'get_stocks @', self.uid, '; error:', e
            pprint(payload)
            pprint(self.headers)
            return False
        else:
            # pprint(self.stocks)
            return self.stocks

    def del_stock(self, code):
        # 在雪球删除指定代码的股票
        try:
            payload = {'code': code}
            response = requests.post(Snowball.url['del'], data=payload, headers=self.headers, timeout=10)
            # pprint(response.content)
            response = response.json()['success']
            if response == True:
                print 'del_stock', code, 'success.'
            else:
                print 'del_stock', code, 'failed.'
        except Exception, e:
            print 'del_stock', code, '@', self.uid, '; error:', e
            pprint(payload)
            pprint(self.headers)
            return False
        else:
            self.get_stocks()
            return response

    def add_stock(self, code):
        # 在雪球添加指定代码的股票
        try:
            payload = {'symbol': code, 'category': 2, 'isnotice': 1}
            response = requests.post(Snowball.url['add'], data=payload, headers=self.headers, timeout=10)
            # pprint(response.content)
            response = response.json()['success']
            if response == True:
                print 'add_stock', code, 'success.'
            else:
                print 'add_stock', code, 'failed.'
        except Exception, e:
            print 'add_stock', code, '@', self.uid, '; error:', e
            pprint(payload)
            pprint(self.headers)
            return False
        else:
            self.get_stocks()
            return response

    def modify_stocks(self, code_list=[]):
        # 雪球自选股列表排序
        try:
            payload = {'pid': -1, 'type': 1, 'stocks': ','.join(code_list)}
            response = requests.post(Snowball.url['modify'], data=payload, headers=self.headers, timeout=10)
            # pprint(response.content)
            response = response.json()['success']
            if response == True:
                print 'modify_stocks', code_list, 'success.'
            else:
                print 'modify_stocks', code_list, 'failed.'
        except Exception, e:
            print 'modify_stocks', code_list, '@', self.uid, '; error:', e
            pprint(payload)
            pprint(self.headers)
            return False
        else:
            self.get_stocks()
            return response


class Tonghuashun:
    # 同花顺自选股列表相关
    url = {'get': 'http://pop.10jqka.com.cn/getselfstockinfo.php',
           'modify': 'http://stock.10jqka.com.cn/self.php'}

    def __init__(self, uid, cookie):
        self.uid = uid
        self.cookie = cookie  # 该用户登录的cookie
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) '
                                      'Gecko/20100101 Firefox/56.0',
                        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                        'Accept-Encoding': 'gzip, deflate',
                        'Referer': 'http://stock.10jqka.com.cn/my/zixuan.shtml',
                        'Cookie': cookie,
                        'DNT': '1'}
        self.stocks = pd.DataFrame()  # 同花顺自选股清单

    def get_stocks(self):
        # 获取同花顺自选股列表
        try:
            payload = {'callback': 'callback' + str(int(time.time() * 1000))}
            response = requests.get(Tonghuashun.url['get'], params=payload, headers=self.headers, timeout=10)
            # pprint(response.content)
            self.stocks = pd.DataFrame(response.json())
        except Exception, e:
            print 'get_stocks @', self.uid, '; error:', e
            pprint(payload)
            pprint(self.headers)
            return False
        else:
            # pprint(self.stocks)
            return self.stocks

    def modify_stock(self, code, method, pos='1'):
        # 更改同花顺自选股列表
        # method: add 添加, del 删除, exc 排序
        # pos: 排序用的序号, 从1开始
        try:
            payload = {'add': {'stockcode': code, 'op': 'add'},
                       'del': {'stockcode': code, 'op': 'del'},
                       'exc': {'stockcode': code, 'op': 'exc', 'pos': pos, 'callback': 'callbacknew'}
                       }
            # self.get_stocks()
            response = requests.get(Tonghuashun.url['modify'], params=payload[method], headers=self.headers, timeout=10)
            # pprint(response.content)
            response = response.content.decode('gbk')
            print 'modify_stocks', method, pos, code, response
            if response == u'修改自选股成功':
                response = True
        except Exception, e:
            print 'modify_stock', method, code, '@', self.uid, '; error:', e
            pprint(payload[method])
            pprint(self.headers)
            return False
        else:
            self.get_stocks()
            return response
