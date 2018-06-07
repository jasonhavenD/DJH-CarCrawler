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
import sys
from urllib import request

if __name__ == '__main__':
	if len(sys.argv)>1:
		if sys.argv[1]=='True':
			print("set headers...")
			headers = {
				"Upgrade-Insecure-Requests": "1",
				"Connection": "keep-alive",
				"Cache-Control": "max-age=0",
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
				"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,la;q=0.7,pl;q=0.6",
				"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
			}
		else:
			print("no headers...")
			headers = {}
	url = "https://www.jianshu.com/"
	try:
		req = request.Request(url=url,headers=headers)
		resp = request.urlopen(req, timeout=5)
		print("success connect to {} !".format(url))
	except Exception as e:
		print(e)
		print("failed....try to bind url {}".format(url))