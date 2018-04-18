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
from urllib import request

headers = {
	"Upgrade-Insecure-Requests": "1",
	"Connection": "keep-alive",
	"Cache-Control": "max-age=0",
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
	"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,la;q=0.7,pl;q=0.6",
	"Accept-Encoding": "gzip, deflate, br",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
}
import io
import gzip
from bs4 import BeautifulSoup
def pre_process_html_doc( html_doc, url, resp):
	try:
		if resp.getheader('Content-Encoding') == 'gzip':
			buf = io.BytesIO(html_doc)
			gf = gzip.GzipFile(fileobj=buf)
			html_doc = gf.read()
		return html_doc
	except Exception as e:
		print(e)
if __name__ == '__main__':
	url = "http://www.chinaautonews.com.cn/list-4-62.html"
	req = request.Request(url=url, headers=headers)
	resp = request.urlopen(req)
	content=resp.read()
	html_doc = pre_process_html_doc(content, url, resp).decode('utf-8')
	soup=BeautifulSoup(html_doc,'lxml')
	if "版权声明"==soup.select_one('h1').text:
		print(soup.select_one('h1').text)

