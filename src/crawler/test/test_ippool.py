#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:test_ippool
   Author:jasonhaven
   date:18-5-31
-------------------------------------------------
   Change Activity:18-5-31:
-------------------------------------------------
"""

import random
def get_random_proxy():
	ips = []
	with open('../../ip_pool/ip_pool.txt', 'r') as f:
		ips = f.readlines()
	ip_port = random.choice(ips).strip()
	ip, port = ip_port.split(u":")[0].strip(), ip_port.split(u":")[1].strip()
	proxy = {'http': 'http://%s:%s' % (ip, port)}
	return proxy


def get_proxies():
	proxies = []
	with open('../../ip_pool/ip_pool.txt', 'r') as f:
		for ip_port in f.readlines():
			ip, port = ip_port.split(u":")[0].strip(), ip_port.split(u":")[1].strip()
			proxy = {'http': 'http://%s:%s' % (ip, port)}
			proxies.append(proxy)
	return proxies

from urllib import request
import time
if __name__ == '__main__':
	urls=['https://www.jianshu.com/','https://www.baidu.com/','http://www.chinaautonews.com.cn/','http://www.autoreport.cn/']
	for url in urls:
		time.sleep(1.5)
		proxy = get_random_proxy()
		proxy_handler = request.ProxyHandler(proxy)
		print("use proxy = {} to crawl url={}".format(proxy,url))

