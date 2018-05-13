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

sys.path.append(os.path.abspath("../util/"))

import log
import tool
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
	# "Accept-Encoding": "gzip, deflate, br",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
}

RE_TRY = 3


class AutoReportCrawler():
	def __init__(self, start=1, end=1):
		self.domain = "http://www.autoreport.cn"
		self.dir = "../../result/autoreport/news"
		self.furls = "../../result/autoreport/urls.lst"
		self.start = start
		self.end = end

	def begin(self, begin=0, end=1):
		self.crawl_page(begin, end)

	def download_html(self, url, retry):
		try:
			req = request.Request(url=url, headers=headers)
			resp = request.urlopen(req, timeout=5)
			if resp.status != 200:
				logger.error('url open error. url = {}'.format(url))
			html_doc = resp.read().decode('utf-8')
			return html_doc
		except Exception as e:
			logger.info("failed....try to bind url {}".format(url))
			if retry > 0:
				return self.download_html(url, retry - 1)

	def crawl_page(self, begin, end):
		clean_html = tool.Clean_html()  # 文本清理工具
		for url in self.urls[begin:end]:
			time.sleep(1.5)
			logger.info("crawling url {}".format(url))
			html_doc = self.download_html(url, RE_TRY)
			soup = BeautifulSoup(html_doc, "lxml")
			article = soup.select_one("article")
			title = clean_html.clean(article.select_one("h1").text)
			text_tag = soup.find('div', attrs={'class': 'article-content'})
			text = ""
			for p in text_tag.find_all('p'):
				text += p.text
			text = clean_html.clean(text)
			self.save_text(title, text, url)

	def crawl_urls(self):
		for x in range(self.start, self.end + 1):
			time.sleep(2)

			urls = []
			url = self.domain + "/newslist/a1169/?pageindex={}".format(x)
			logger.info("crawling urls from page {}".format(x))

			# 使用IP池
			# proxy = tool.get_random_proxy()
			# logger.info("proxy = {}".format(proxy))
			# proxy_handler = request.ProxyHandler(proxy)
			# opener = request.build_opener(proxy_handler)
			# request.install_opener(opener)

			req = request.Request(url=url, headers=headers)
			resp = request.urlopen(req, timeout=5)
			if resp.status != 200:
				logger.error('url open error. url = {}'.format(url))
			# html_doc = self.pre_process_html_doc(resp.read(), url, resp)
			html_doc = resp.read().decode('utf-8')
			soup = BeautifulSoup(html_doc, "lxml")

			article_cards = soup.find_all("div", attrs={"class": "article-card-box"})[0].find_all("div", attrs={
				"class": "article-card"})
			for article in article_cards:
				href = article.select_one("a").get('href')
				url = self.domain + href
				urls.append(url)
			self.save_urls(list(set(urls)), x)  # url去重

	def save_text(self, title, text, href):
		p = re.compile('\W')
		title = re.sub(p, '', title)
		if len(title) > 10:
			title = title[:10]
		file = self.dir + os.sep + title + '.txt'
		with codecs.open(file, 'w', encoding='utf-8') as f:
			f.write(text)
			logger.info("text of {} has all saved as {}!".format(href, file))

	def save_urls(self, urls, number):
		with codecs.open(self.furls, 'a', encoding='utf-8') as f:
			f.write("\n".join(urls))
			f.write('\n')
			logger.info("page {} has been saved !".format(number))

	def load_urls(self):
		with codecs.open(self.furls, 'r', encoding='utf-8') as f:
			self.urls = f.readlines()
			return self.urls


class MyThread(threading.Thread):
	def __init__(self, threadID, name, crawler, begin, end):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.crawler = crawler
		self.begin = begin
		self.end = end

	def run(self):
		logger.info("start thread...:" + self.name)
		self.crawler.begin(self.begin, self.end)
		logger.info("stop thread...:" + self.name)


if __name__ == '__main__':
	logger.info("start to crawl http://www.autoreport.cn")

	a = 0
	b = 50

	crawler = AutoReportCrawler(a, b)
	# 爬取urls
	# crawler.crawl_urls()
	# 加载urls
	urls = crawler.load_urls()
	# crawler.crawl_page(a, b)

	begin = datetime.datetime.now()
	# 三个爬虫爬取
	start = 0
	middle1 = int(len(urls) / 3)
	middle2 = int(2 * len(urls) / 3)
	end = len(urls) - 1

	# logger.info("{},{},{},{}".format(start, middle1, middle2, end))

	thread1 = MyThread(1, 'crawler 1', crawler, start, middle1)
	thread2 = MyThread(2, 'crawler 2', crawler, middle1, middle2)
	thread3 = MyThread(3, 'crawler 3', crawler, middle2, end)

	thread1.start()
	thread2.start()
	thread3.start()

	thread1.join()
	thread2.join()
	thread3.join()
	end = datetime.datetime.now()
	logger.info('finished crawl pages of [{},{}] in {}s'.format(a, b, end - begin))
