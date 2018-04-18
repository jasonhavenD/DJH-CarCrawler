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
import os
import gzip
import io
import codecs
import urllib
from urllib import request
from bs4 import BeautifulSoup
import time

logger = log.Logger().get_logger()
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

domain = 'https://club.autohome.com.cn/'


def save_home_urls(dir, all_urls):
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


def crawl_home_urls():
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

	save_home_urls("F:\BiShe\workspace\github\DJH-CarCrawler/result/autohome/homeurls", all_urls)


# def save_file(file, type, text):
# 	path = file + type
# 	file = open(path, 'w')
# 	file.truncate()  # 清空文件
# 	file.close()
#
# 	with codecs.open(path, "a", encoding='utf-8') as f:
# 		f.write(text)
# 	logger.info("{} has been saved!".format(path))

def save_brandjx_urls(file, all_urls):
	with codecs.open(file, 'w', encoding='utf-8') as f:
		f.writelines(all_urls)
		logger.info("urls of {} has all saved!".format(file))


def crawl_brandjx_url(forum, url):
	logger.info('crawl_brandjx_url url={}'.format(url))
	# 使用IP池
	proxy = tool.get_random_proxy()
	proxy_handler = request.ProxyHandler(proxy)
	opener = request.build_opener(proxy_handler)
	request.install_opener(opener)
	time.sleep(3)
	try:
		# opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
		# resp = opener.open(url)

		req = urllib.request.Request(url=url, headers=headers)
		resp = urllib.request.urlopen(req)

		if resp.status != 200:
			print("not 200!")

		content = resp.read()
		if resp.getheader('Content-Encoding') == 'gzip':
			buf = io.BytesIO(content)
			gf = gzip.GzipFile(fileobj=buf)
			content = gf.read()
		soup = ""
		if content != None:
			soup = BeautifulSoup(content, "lxml")
		else:
			logger.error("content is None!")
			return None

		if forum == "车系论坛":
			# 品牌论坛
			ul = soup.find("div", attrs={"class": "tabarea motor-tabarea"}).select_one("ul")
			brand_link = ul.find_all("li")[1].select_one("a")
			if '品牌论坛' == brand_link.string.strip():
				brand_url = brand_link.get("href")
				# 论坛精华帖
				if brand_url != None:
					brandjx = brand_url.replace('brand', 'brandjx')
				logger.info("forum:{} brandjx={}".format(forum, brandjx))
				return brandjx
			return None
		else:
			brand_link = soup.find('li', attrs={'id': 'btnNavJinghua'})
			if '论坛精华帖' == brand_link.string.strip():
				brand_url = brand_link.get("href")
				if brand_url != None:
					brandjx = brand_url
					return brandjx
			return None
		return None
	except urllib.request.URLError as e:
		logger.error(e)
	except Exception as e:
		logger.error("{}: url = {}".format(e, url))


if __name__ == '__main__':
	dir = "F:\BiShe\workspace\github\DJH-CarCrawler/result/autohome/homeurls"
	output = "F:\BiShe\workspace\github\DJH-CarCrawler/result/autohome/brandjxurls/品牌论坛精华帖.lst"
	all_urls = []
	for parent, dir_names, file_names in os.walk(dir):
		for file_name in file_names:
			f = dir + os.sep + file_name
			with codecs.open(f, 'r', encoding='utf-8') as f:
				for item in f.readlines()[:5]:
					name, url = item.split('\t')
					if name.find('/') != -1:
						name = name.replace('/', '-')
					forum = file_name
					url = crawl_brandjx_url(forum, domain + url)
					if url != None:
						all_urls.append(url)
	all_urls = set(all_urls)
	save_brandjx_urls(output, all_urls)
