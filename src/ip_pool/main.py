#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:main
   Author:jasonhaven
   date:2018/4/18
-------------------------------------------------
   Change Activity:2018/4/18:
-------------------------------------------------
"""
import IPCrawler
import time


#https://zhuanlan.zhihu.com/p/25285987

if __name__ == '__main__':
	url = 'http://www.xicidaili.com/nn/'
	url_list = IPCrawler.get_url(url, nums=3)
	for i in url_list:
		print(i)
		content = IPCrawler.get_content(i)
		time.sleep(1.5)
		IPCrawler.get_info(content)

	test_url = "https://www.baidu.com"  # 自定义
	url_list=[]
	with open("proxies.txt", "r") as fd:
		url_list = fd.readlines()
	for data in url_list:
		IPCrawler.verif_ip(data.split(u":")[0].strip(), data.split(u":")[1].strip(), test_url)
