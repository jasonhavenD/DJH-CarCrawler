#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:main
   Author:jasonhaven
   date:2018/4/17
-------------------------------------------------
   Change Activity:2018/4/17:
-------------------------------------------------
"""

import log
import tool
import gzip
import io
import os
import codecs
import re
import time
import datetime
import threading
from urllib import request
from bs4 import BeautifulSoup

logger = log.Logger().get_logger()

headers = {
	"Upgrade-Insecure-Requests": "1",
	"Connection": "keep-alive",
	"Cache-Control": "max-age=0",
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
	"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,la;q=0.7,pl;q=0.6",
	"Accept-Encoding": "gzip, deflate, br",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
}


class ChinaautonewsCrawler():
	TYPE = ["domestic", "inter", "news"]

	def __init__(self, type, url_middle):
		self.domain = "http://www.chinaautonews.com.cn/"
		if type in self.TYPE:
			self.type = type
		else:
			logger.error("type is not right!")
		self.url_middle = url_middle

	def crawl_page(self, url):
		req = request.Request(url=url, headers=headers)
		resp = request.urlopen(req)
		if resp.status != 200:
			logger.error('url open error. url = {}'.format(url))
		html_doc = self.pre_process_html_doc(resp.read(), url, resp)
		soup = BeautifulSoup(html_doc, "lxml")
		clean_html = tool.Clean_html()
		title = soup.select_one('h1').string
		text_tag = soup.find('div', attrs={'class': 'detail-content'})
		text = ""
		for p in text_tag.find_all('p'):
			text += p.text
		return title, clean_html.clean(text)

	def save_text(self, title, text, href):
		dir = '../../result/chinaautonews/' + self.type
		file = dir + os.sep + title + '.txt'
		with codecs.open(file, 'w', encoding='utf-8') as f:
			f.write(text)
			logger.info("text of {} has all saved as {}!".format(href, file))

	def pre_process_html_doc(self, html_doc, url, resp):
		try:
			if resp.getheader('Content-Encoding') == 'gzip':
				buf = io.BytesIO(html_doc)
				gf = gzip.GzipFile(fileobj=buf)
				html_doc = gf.read()
			return html_doc
		except Exception as e:
			logger.error("{}: url = {}".format(e, url))

	def begin(self, start_page=0, end_page=10):
		start_url = self.domain + "list-13-" + str(start_page) + ".html"
		url = start_url
		next_page = start_page
		begin = datetime.datetime.now()
		number = 1
		while (next_page < end_page):
			next_page += 1
			url = self.domain + "list-13-" + str(next_page) + ".html"

			# 使用IP池
			# proxy = tool.get_random_proxy()
			# logger.info("proxy = {}".format(proxy))
			# proxy_handler = request.ProxyHandler(proxy)
			# opener = request.build_opener(proxy_handler)
			# request.install_opener(opener)

			req = request.Request(url=url, headers=headers)
			resp = request.urlopen(req)
			time.sleep(1)
			if resp.status != 200:
				logger.error('url open error. url = {}'.format(start_url))
			html_doc = self.pre_process_html_doc(resp.read(), url, resp)
			soup = BeautifulSoup(html_doc, "lxml")
			li_tags = soup.find("div", attrs={"class": "lside_nr"}).find_all("li")
			for li in li_tags:
				href = li.select_one('a').get('href')
				if not href.startswith('http://www.chinaautonews.com.cn/show'):
					continue
				logger.info("crawling page {} url = {}".format(next_page, href))
				title, text = self.crawl_page(href)
				name = str(number) + "-" + re.sub(re.compile(r'["/ ]'), '_', title)[:2]
				number += 1
				self.save_text(name, text, href)
		end = datetime.datetime.now()
		print('finished in ' + str((end - begin).seconds) + ' s!')


class MyThread(threading.Thread):
	def __init__(self, threadID, name, crawler, start_page=0, end_page=20):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.crawler = crawler
		self.start_page = start_page
		self.end_page = end_page

	def run(self):
		logger.info("start thread...:" + self.name)
		self.crawler.begin(self.start_page, self.end_page)
		logger.info("stop thread...:" + self.name)


if __name__ == '__main__':
	url_middles_dict = {
		"news": "list-6-",
		"inter": "list-14-",
		"domestic": "list-13-"
	}

	news_crawler = ChinaautonewsCrawler("news", url_middles_dict["news"])
	inter_crawler = ChinaautonewsCrawler("inter", url_middles_dict["inter"])
	domestic_crawler = ChinaautonewsCrawler("domestic", url_middles_dict["domestic"])

	news_crawler.begin(0,130)

	# thread_news = MyThread(1, "news_crawler", news_crawler, 0, 130)
	# thread_inter = MyThread(2, "inter_crawler", inter_crawler, 0, 45)
	# thread_domestic = MyThread(3, "domestic_crawler", domestic_crawler, 0, 60)
	#
	# thread_news.start()
	# thread_inter.start()
	# thread_domestic.start()
	#
	# thread_news.join()
	# thread_inter.join()
	# thread_domestic.join()
