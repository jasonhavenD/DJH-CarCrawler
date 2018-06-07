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
import sys
import os

sys.path.append(os.path.abspath('../util/'))

import log
import tool
import gzip
import io

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

url_middles_dict = {
	"news": "list-6-",  # 新闻
	"inter": "list-14-",  # 国际
	"domestic": "list-13-",  # 国内
	"newcar": "list-7-"  # 国内
}

RE_TRY = 3


class ChinaautonewsCrawler():
	TYPE = url_middles_dict.keys()

	def __init__(self, type, url_middle):
		self.domain = "http://www.chinaautonews.com.cn/"
		if type in self.TYPE:
			self.type = type
		else:
			logger.error("type is not right!")
		self.url_middle = url_middle
		self.urls = []

	def download_html(self, url, retry):
		time.sleep(1.5)
		try:
			req = request.Request(url=url, headers=headers)
			resp = request.urlopen(req, timeout=5)
			if resp.status != 200:
				logger.error('url open error. url = {}'.format(url))
			html_doc = resp.read()
			return html_doc
		except Exception as e:
			logger.info("failed....try to bind url {}".format(url))
			if retry > 0:
				return self.download_html(url, retry - 1)

	def crawl_page(self, url):
		req = request.Request(url=url, headers=headers)
		resp = request.urlopen(req, timeout=5)
		if resp.status != 200:
			logger.error('url open error. url = {}'.format(url))
		html_doc = self.download_html(url, RE_TRY)
		html_doc = self.pre_process_html_doc(html_doc, url, resp)
		soup = BeautifulSoup(html_doc, "lxml")

		title = soup.select_one("h1")
		if title != None and title.text.strip() == "版权声明":
			logger.info(("版权声明"))
			return None, None

		clean_html = tool.Clean_html()
		title = soup.select_one('h1').string
		text_tag = soup.find('div', attrs={'class': 'detail-content'})
		text = ""
		for p in text_tag.find_all('p'):
			text += p.text
		self.save_url(url)
		return title, clean_html.clean(text)

	def save_text(self, title, text, href):
		dir = '../../result/chinaautonews/' + self.type
		file = dir + os.sep + title + '.txt'
		with codecs.open(file, 'w', encoding='utf-8') as f:
			f.write(text)
			logger.info("text of {} has all saved as {}!".format(href, file))

	def save_url(self, url):
		file = '../../result/chinaautonews/urls.lst'
		with codecs.open(file, 'a', encoding='utf-8') as f:
			f.write(url)
			f.write("\n")
			logger.info("url {} has been saved !".format(url))

	def pre_process_html_doc(self, html_doc, url, resp):
		try:
			if resp.getheader('Content-Encoding') == 'gzip':
				buf = io.BytesIO(html_doc)
				gf = gzip.GzipFile(fileobj=buf)
				html_doc = gf.read()
			return html_doc.decode('utf-8')
		except Exception as e:
			logger.error("{}: url = {}".format(e, url))

	def begin(self, start_page=0, end_page=10):
		begin = datetime.datetime.now()
		number = 1
		# if self.urls != []:
		# logger.info("crawl from using cached urls.lst")
		# for url in self.urls:
		# 	time.sleep(3)
		# 	title, text = self.crawl_page(url)
		# 	if title == None or text == None:
		# 		logger.info("filter url = {}".format(url))
		# 		continue
		# 	name = str(number) + "-" + re.sub(re.compile(r'["/ ]'), '_', title)[:2]
		# 	number += 1
		# 	self.save_text(name, text, url)
		# end = datetime.datetime.now()
		# print('finished in ' + str((end - begin).seconds) + ' s!')
		# else:
		next_page = start_page
		while (next_page < end_page):
			next_page += 1
			url = self.domain + self.url_middle + str(next_page) + ".html"

			# 使用IP池
			# proxy = tool.get_random_proxy()
			# logger.info("proxy = {}".format(proxy))
			# proxy_handler = request.ProxyHandler(proxy)
			# opener = request.build_opener(proxy_handler)
			# request.install_opener(opener)

			req = request.Request(url=url, headers=headers)
			resp = request.urlopen(req, timeout=5)

			time.sleep(3)

			if resp.status != 200:
				logger.error('url open error. url = {}'.format(url))
			html_doc = self.pre_process_html_doc(resp.read(), url, resp)
			soup = BeautifulSoup(html_doc, "lxml")

			li_tags = soup.find("div", attrs={"class": "lside_nr"}).find_all("li")

			for li in li_tags:
				href = li.select_one('a').get('href')
				if not href.startswith('http://www.chinaautonews.com.cn/show'):
					continue
				logger.info("crawling page {} url = {}".format(next_page, href))

				time.sleep(2)

				title, text = self.crawl_page(href)

				if title == None or text == None:
					logger.info("filter url = {}".format(href))
					continue

				name = str(number) + "-" + re.sub(re.compile(r'["/ ]'), '_', title)[:2]
				number += 1
				self.save_text(name, text, href)
		end = datetime.datetime.now()
		print('finished in ' + str((end - begin).seconds) + ' s!')

	def load_urls(self):
		path = "../../result/chinaautonews/urls.lst"
		with codecs.open(path, 'r', encoding="utf-8") as f:
			self.urls = set(f.readlines())


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
	logger.info("start to crawl http://www.chinaautonews.com.cn/")
	logger.info("start to crawl new mudle")
	logger.info("start to crawl international mudle")
	logger.info("start to crawl domestic mudle")
	logger.info("start to crawl newcar mudle")

	a = 0
	b = 5

	begin = datetime.datetime.now()
	news_crawler = ChinaautonewsCrawler("news", url_middles_dict["news"])
	inter_crawler = ChinaautonewsCrawler("inter", url_middles_dict["inter"])
	domestic_crawler = ChinaautonewsCrawler("domestic", url_middles_dict["domestic"])
	newcar_crawler = ChinaautonewsCrawler("newcar", url_middles_dict["newcar"])

	thread_news = MyThread(1, "news_crawler", news_crawler, a, b)
	thread_inter = MyThread(2, "inter_crawler", inter_crawler, a, b)
	thread_domestic = MyThread(3, "domestic_crawler", domestic_crawler, a, b)
	thread_newcar = MyThread(4, "newcar_crawler", newcar_crawler, a, b)

	thread_news.start()
	thread_inter.start()
	thread_domestic.start()
	thread_newcar.start()

	thread_news.join()
	thread_inter.join()
	thread_domestic.join()
	thread_newcar.join()

	end = datetime.datetime.now()
	logger.info('finished crawl pages of [{},{}] in {}s'.format(a, b*20, end - begin))
