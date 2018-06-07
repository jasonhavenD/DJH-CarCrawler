#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:test_header
   Author:jasonhaven
   date:18-5-31
-------------------------------------------------
   Change Activity:18-5-31:
-------------------------------------------------
"""
import time
from urllib import request
headers = {
	"Upgrade-Insecure-Requests": "1",
	"Connection": "keep-alive",
	"Cache-Control": "max-age=0",
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
	"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,la;q=0.7,pl;q=0.6",
	# "Accept-Encoding": "gzip, deflate, br",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
}


def conn(url, retry):
	time.sleep(3)
	try:
		req = request.Request(url=url, headers=headers)
		resp = request.urlopen(req, timeout=5)
		if resp.status != 200:
			print('url open error. url = {}'.format(url))
		html_doc = resp.read().decode('utf-8')
		return html_doc
	except:
		print("failed....try to bind url {}".format(url))
		if retry > 0:
			return conn(url, retry - 1)


if __name__ == '__main__':
	url = "https://www.baidu.com"
	flag = conn(url=url, retry=3)
	if flag!=None:
		print("success conn to {}!".format(url))