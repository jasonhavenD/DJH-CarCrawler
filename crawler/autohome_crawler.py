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
from urllib import request
from bs4 import BeautifulSoup

# class AutohomeCrawler():
# 	def __init__(self):
# 		pass
#
# 	def start(self):
# 		pass
#
# 	def stop(self):
# 		pass

import log
import os
import chardet
import gzip
import io
import codecs

logger = log.Logger().get_logger()

domain = 'https://club.autohome.com.cn/'
headers = {
	"Accept-Encoding": "gzip",
	"Cache-Control": "max-age=0",
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
	"Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,en-US;q=0.4,zh-TW;q=0.2",
	"Connection": "keep-alive",
	"Accept-Encoding": "gzip, deflate",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}


def save_urls(dir, all_urls):
	dir = "F:\BiShe\workspace\github\DJH-CarCrawler/result/autohome/urls"
	try:
		if os.path.exists(dir) is False:
			os.makedirs(dir)
			logger.info("dir:{} has been created!".format(dir))
	except Exception:
		logger.error("can not make dirs filepath is {} ".format(dir))
	for key, hrefs in all_urls.items():
		with codecs.open(dir + os.sep + str(key) + ".lst", "w", encoding='utf-8') as f:
			f.writelines('\n'.join(hrefs))
		logger.info("urls of {} has all saved!".format(key))


def crawl_to_urls():
	start_url = domain
	req = request.Request(url=start_url, headers=headers)
	resp = request.urlopen(req)
	if resp.status != 200:
		logger.error('url open error. url = {}'.format(start_url))
	content = resp.read()
	try:
		if resp.getheader('Content-Encoding') == 'gzip':
			buf = io.BytesIO(content)
			gf = gzip.GzipFile(fileobj=buf)
			content = gf.read()
	except Exception as e:
		logger.error("{}: url = {}".format(e, start_url))
	soup = BeautifulSoup(content, "lxml")

	# 保存全部的urls
	all_urls = {}

	# 车系论坛
	div = soup.find("div", attrs={'id': 'tab-4'})
	all_urls['车系论坛'] = []
	forum_brand_box = div.find("div", attrs={'class': 'forum-brand-box'})
	if forum_brand_box != None:
		urls = forum_brand_box.find_all('ul', attrs={'class': 'forum-list02'})
		if urls != None:
			for url in urls:
				links = url.find_all('a')
				titles = [link.string for link in links]
				hrefs = [link['href'] for link in links]
				all_urls['车系论坛'].extend(["{}\t{}".format(t, h) for t, h in zip(titles, hrefs)])

	# 地区论坛
	div = soup.find("div", attrs={'id': 'tab-5'})
	forum_tab = div.find('div', attrs={'class': 'forum-tab-box'})
	links = forum_tab.find_all('a')
	titles = [link.string for link in links]
	hrefs = [link['href'] for link in links]
	all_urls['地区论坛'] = ["{}\t{}".format(t, h) for t, h in zip(titles, hrefs)]

	# 主题论坛
	div = soup.find("div", attrs={'id': 'tab-6'})
	forum_tab = div.find('ul', attrs={'class': 'forum-list'})
	links = forum_tab.find_all('a')
	titles = [link.string for link in links]
	hrefs = [link['href'] for link in links]
	all_urls['主题论坛'] = ["{}\t{}".format(t, h) for t, h in zip(titles, hrefs)]

	# 摩托车论坛
	div = soup.find("div", attrs={'id': 'tab-7'})
	forum_tab = div.find('ul', attrs={'class': 'forum-list'})
	links = forum_tab.find_all('a')
	titles = [link.string for link in links]
	hrefs = [link['href'] for link in links]
	all_urls['摩托车论坛'] = ["{}\t{}".format(t, h) for t, h in zip(titles, hrefs)]

	save_urls('', all_urls)


def crawl_from_url(dir, name, url):
	path = dir + os.sep + name
	logger.info("save {} to {}".format(url, path))


if __name__ == '__main__':
	dir = "F:\BiShe\workspace\github\DJH-CarCrawler/result/autohome"
	dir_urls = dir + os.sep + 'urls'
	dir_files = dir + os.sep + 'files'
	input_urls = []
	output_files = []
	# 创建相应目录存放爬取结果
	for parent, dir_names, file_names in os.walk(dir_urls):
		for file_name in file_names:
			dir_path = dir_files + os.sep + file_name[:file_name.rindex('.')] + os.sep
			input_urls.append(dir_urls + os.sep + file_name)
			output_files.append(dir_path)
			try:
				if os.path.exists(dir_path) is False:
					os.makedirs(dir_path)
					logger.info("dir:{} has been created!".format(dir_path))
			except Exception as e:
				logger.error("can not make dirs filepath is {} {}".format(dir, e))
	# print(input_urls)
	# print(output_files)



	# 爬取url
	for dir, furl in zip(output_files, input_urls):
		name_urls = []
		with codecs.open(furl, 'r', encoding='utf-8') as f:
			name_urls = f.readlines()

		for item in name_urls:
			name, url = item.split('\t')
			crawl_from_url(dir, name, url)
