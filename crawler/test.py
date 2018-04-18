#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:test
   Author:jasonhaven
   date:2018/4/18
-------------------------------------------------
   Change Activity:2018/4/18:
-------------------------------------------------
"""
import urllib.request
import urllib
import io
import gzip
from bs4 import BeautifulSoup

if __name__ == '__main__':
	url = "https://club.autohome.com.cn/bbs/forum-o-200202-1.html"
	headers = {
		"Host": "club.autohome.com.cn",
		"Referer": "https://club.autohome.com.cn/",
		"Upgrade-Insecure-Requests": "1",
		"Connection": "keep-alive",
		"Cache-Control": "max-age=0",
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
		"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,la;q=0.7,pl;q=0.6",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
	}

	# opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
	# resp = opener.open(url)
	req = urllib.request.Request(url=url, headers=headers)
	resp = urllib.request.urlopen(req)
	if resp.status != 200:
		print("not 200!")
	content = resp.read()
	try:
		if resp.getheader('Content-Encoding') == 'gzip':
			buf = io.BytesIO(content)
			gf = gzip.GzipFile(fileobj=buf)
			content = gf.read()
		soup = BeautifulSoup(content, "lxml")
		brand_link = ""
		brand_url = ""
		brandjx = ""
		brand_link = soup.find('li', attrs={'id': 'btnNavJinghua'})
		print(brand_link)
		if '论坛精华帖' == brand_link.string.strip():
			brand_url = brand_link.get("href")
		if brand_url != None:
			brandjx = brand_url
		print(brandjx)
	except Exception as e:
		print(e)
