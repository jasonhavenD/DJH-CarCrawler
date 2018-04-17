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
import os
from util.io import IOHelper
from util.log import Logger
from util.const import const

if __name__ == '__main__':
	logger = Logger(True).get_logger()
	logger.info("info")
	logger.debug("debug")
	logger.error("error")

	io = IOHelper()
	io.read('', '', '')
	io.write('', '', '')

	print(const.DOMAIN_OF_AUTOHOME)
