#!/usr/bin/env python
# encoding: utf-8
"""
@author: zlm
@time: 2016-09-20 15:47
"""
import logging
import random
from ..sql.mssql import MSSQL

logger = logging.getLogger('proxy')


class Proxy:

    def __init__(self):
        self._ms = MSSQL('host', 'username', 'password', 'db')

    def get_random_proxies(self):
        # 从代理数据库随机拿
        sql_model = 'SELECT proxy,port FROM [ProxyData].[dbo].[TempProxy] where proxy_id={0}'
        while True:
            rand_int = random.choice(range(1, 60))
            new_sql = sql_model.format(rand_int)
            res_list = self._ms.ExecQuery(new_sql)
            if res_list:
                res_poxy = res_list[0]
                return {'ip': res_poxy[0], 'port': res_poxy[1]}
            else:
                logger.info('not find proxy')

    def delete_proxy(self, proxy):
        # print proxy
        src_ip = proxy.split('/')[-1]
        logger.info('{0} is deleted'.format(src_ip))

