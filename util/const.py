#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:Configer
   Author:jasonhaven
   date:2018/4/17
-------------------------------------------------
   Change Activity:2018/4/17:
-------------------------------------------------
"""


class _const:
	class ConstError(TypeError):
		pass

	class ConstCaseError(ConstError):
		pass

	def __setattr__(self, name, value):
		if name in self.__dict__:
			raise self.ConstError("can't change const %s" % name)
		if not name.isupper():
			raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
		self.__dict__[name] = value


const = _const()

const.HEADERS = {
	"Accept-Encoding": "gzip",
	"Cache-Control": "max-age=0",
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
	"Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,en-US;q=0.4,zh-TW;q=0.2",
	"Connection": "keep-alive",
	# "Accept-Encoding": "gzip, deflate",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

# 汽车之家
const.DOMAIN_OF_AUTOHOME = 'https://club.autohome.com.cn/'
