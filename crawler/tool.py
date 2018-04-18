#! /usr/bin/env/python
#
# coding utf-8
#
# jasonahven
#


import random


def get_random_proxy():
	ips = []
	with open('IPPool\ip_pool.txt', 'r') as f:
		ips = f.readlines()
	ip_port = random.choice(ips).strip()
	ip, port = ip_port.split(u":")[0].strip(), ip_port.split(u":")[1].strip()
	proxy = {'http': 'http://%s:%s' % (ip, port)}
	return proxy

if __name__ == '__main__':
    print(get_random_proxy())