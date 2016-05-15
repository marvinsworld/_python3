# -*- coding: UTF-8 -*-
# -*- author: Eason -*-
# -*- date: 2015-12-22 22:38 -*-
# !/usr/bin/python
import urllib


class BaiduCrawler():

    def crawler(self):
        #http = urllib.PoolManager()
        reponse = urllib.request.urlopen('http://wwww.baidu.com')
        data = reponse.read()
        print(data)


if __name__ == "__main__":
    BaiduCrawler().crawler()