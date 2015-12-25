# -*- coding: UTF-8 -*-
# -*- author: Eason -*-
# -*- date: 2014-10-21 23:15 -*-
#!/usr/bin/python
import re
from bs4 import BeautifulSoup
import mysql.connector
import urllib3
from com.eason.web.crawler.BaseCrawler import BaseCrawler

#分类抓取类
class CatCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()

    #抓取分类
    def crawlCat(self):
        http = urllib3.PoolManager()
        r = http.request('GET', 'http://www.jd.com/allSort.aspx')
        data = r.data.decode("gbk")

        soup = BeautifulSoup(data) # html为html源代码字符串，type(html) == str
        content = soup.find("div", {"id": "allsort"})

        contents = content.findAll("a", {"href": re.compile("^http://list.jd.com/")})

        data = []
        for cat in contents:
            data.append((cat.get('href'), cat.string.__str__()))
        return data

    #持久化
    def persistent(self, data):
        config = {'host': 'localhost', #默认127.0.0.1
                  'user': 'root',
                  'password': 'root',
                  'port': 3306, #默认即为3306
                  'database': 'test',
                  'charset': 'utf8'#默认即为utf8
        }

        cnn = mysql.connector.connect(**config)
        cursor = cnn.cursor()
        stmt = "insert into cat (cat, name) values (%s, %s)"

        try:
            cursor.executemany(stmt, data)
            cnn.commit()
        finally:
            cursor.close()
            cnn.close()

if __name__ == '__main__':
    catCrawler = CatCrawler()
    data = catCrawler.crawlCat()
    print(data)
    catCrawler.persistent(data)