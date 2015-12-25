# -*- coding: UTF-8 -*-
# -*- author: Eason -*-
# -*- date: 2014-10-21 23:25 -*-
#!/usr/bin/python
import urllib3
from com.eason.web.crawler.BaseCrawler import BaseCrawler

#搜索结果抓取
class CatSearchCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()

    #抓取url全文
    def crawlUrl(self, url):
        url = 'http://list.jd.com/670-686-1047.html'
        http = urllib3.PoolManager()
        r = http.request('GET', url)
        content = r.data.decode("utf-8")
        return content

    #解析商品列表
    def parseSku(self, content):
        print("")
        #skuid,price,time

if __name__ == "__main__":
    crawler = CatSearchCrawler()
    crawler.crawlUrl("")

