#!/usr/bin/env python
# encoding: utf-8
"""
@author: zlm
@time: 2016-09-20 15:47
"""
import datetime
import logging
import random

import requests
import time

logger = logging.getLogger('proxy')


class Proxy:

    def __init__(self):
        self.proxies = []
        self.timestamp = datetime.datetime.now()

    def _get_proxies(self):
        res = None
        while True:
            # 代理供应商 api
            res = requests.get('http://s.zdaye.com/')
            self.timestamp = datetime.datetime.now()
            if res.text.find(u'</bad>') != -1:
                time.sleep(3)
            else:
                break
        rlist = res.text.split('\r\n')
        res_list = [each.split(':') for each in rlist]
        for each in res_list:
            self.proxies.append({'ip': each[0], 'port': str(each[1])})

    def get_random_proxies(self):
        delta = datetime.datetime.now() - self.timestamp
        if not self.proxies or delta.seconds >= 120:
            self.proxies = []
            self._get_proxies()
        # 方法1: 用一次就扔
        return self.proxies.pop()
        # 方法2: 随机使用 删除无效的
        # return random.choice(self.proxies)

    def delete_proxy(self, proxy):
        # print proxy
        src_ip = proxy.split('/')[-1]
        for each in self.proxies:
            des = each['ip'] + ':' + each['port']
            if des == src_ip:
                print(proxy, 'delete')
                # 删除无效的 ip
                self.proxies.remove(each)

