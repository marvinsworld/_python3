# -*- coding: UTF-8 -*-
# -*- author: Eason -*-
# -*- date: 2014-10-21 23:25 -*-
#!/usr/bin/python
import re
from bs4 import BeautifulSoup
from com.eason.web.crawler.BaseCrawler import BaseCrawler

from com.marvinsworld.common import Common

class RootCrawler(BaseCrawler):
    RootPath = "E:\\pages\\"
    RootUrl = "http://wiki.corp.qunar.com"

    def __init__(self):
        super().__init__()


    #抓取根页面中的空间的table
    def parseSpaceTable(self, url):
        print(url)
        content = Common.crawlUrl(url)
        soup = BeautifulSoup(content)
        tableNode = soup.find("table", attrs={'class': "spaceList"})
        self.findAllLink(tableNode)
        self.saveRootHtml(url, tableNode.__str__())


    #查询所有的链接节点
    def findAllLink(self, node):
        links = node.find_all("a", attrs={'class': "fontSizeDefault"})

        for link in links:
            shortUrl = link["href"] #/display/fe
            path = "%s%s" % (self.RootPath, shortUrl)
            Common.mkdir(path)

            fullUrl = "%s%s" % (self.RootUrl, shortUrl)
            print("Crawl Url=%s" % fullUrl)
            content = Common.crawlUrl(fullUrl)
            self.saveHomeHtml(path, content)

    #保存home页面
    def saveHomeHtml(self, path, content):
        str = "<meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\">\n"\
              "<link type=\"text/css\" rel=\"stylesheet\" href=\"../../css/batch.css\">\n"\
              "<link type=\"text/css\" rel=\"stylesheet\" href=\"../../css/colors.css\">\n"\
              "<link type=\"text/css\" rel=\"stylesheet\" href=\"../../css/custom.css\">\n"\
              "<link type=\"text/css\" rel=\"stylesheet\" href=\"../../css/default-theme.css\">\n"\
              "<link type=\"text/css\" rel=\"stylesheet\" href=\"../../css/splitter.css\">\n"

        content = str + content
        Common.savePage(path + "/home.html", content)


    #指定的url替换为.html
    def replaceLink(self, content):
        content = re.sub(r"(<a class=\"fontSizeDefault\" href=\")/(.*?)\"", "\g<1>\g<2>/home.html\"", content)
        return content


    #保存为root.html
    def saveRootHtml(self, url, content):
        content = self.replaceLink(content)

        path = "%sroot.html" % self.RootPath

        #增加编码
        content = "<meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\">" + content

        Common.savePage(path, content)
        print("File Saved Success.url=%s ,path=%s" % (url, path))


    #所有home节点url
    def getHomeLink(self, url):
        content = Common.crawlUrl(url)
        soup = BeautifulSoup(content)
        tableNode = soup.find("table", attrs={'class': "spaceList"})
        links = tableNode.find_all("a", attrs={'class': "fontSizeDefault"})

        homeLinks = []
        for link in links:
            shortUrl = link["href"] #/display/fe
            homeLinks.append(shortUrl)

        return homeLinks


if __name__ == "__main__":
    crawler = RootCrawler()
    crawler.parseSpaceTable("http://wiki.corp.qunar.com/dashboard.action")
    #print(crawler.getHomeLink("http://wiki.corp.qunar.com/dashboard.action"))