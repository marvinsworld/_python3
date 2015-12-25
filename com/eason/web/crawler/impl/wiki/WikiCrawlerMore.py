# -*- coding: UTF-8 -*-
# -*- author: Eason -*-
# -*- date: 2014-10-21 23:25 -*-
#!/usr/bin/python
import re
import urllib.parse
from bs4 import BeautifulSoup
from com.eason.web.crawler.BaseCrawler import BaseCrawler
from com.eason.web.crawler.impl.wiki.RootCrawler import RootCrawler
from com.marvinsworld.common import Common

#抓取页面
class WikiCrawlerMore(BaseCrawler):
    RootPath = "D:\\pages\\"

    def __init__(self):
        super().__init__()


    #解析home页面
    def crawlHomePage2(self, path):
        fulluUrl = "http://wiki.corp.qunar.com%s" % path
        print(fulluUrl)
        content = Common.crawlUrl(fulluUrl)
        soup = BeautifulSoup(content)
        pageId = soup.find("input", id="pageId")["value"]
        print("Home解析后的id=%s,url=%s" % (pageId, fulluUrl))
        self.crawlOneLevel2(pageId, path)

        #allContent = "<meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\">\n" + allContent
        #Common.savePage(self.RootPath + path + "/index.html", allContent)
        #Common.savePage("D://pages/display/flight/index.html", allContent)


    #解析尾部
    def commonParseTail(self, url):
        regMatch = re.compile("(.*)\?pageId=(\d+)").search(url)

        if regMatch:
            id = regMatch.groups()[1]
        else:
            #不匹配取尾部
            id = url[url.rfind("/") + 1:]
        return id


    #抓取全部层级
    def crawlOneLevel2(self, pageId, path):
        #print(pageId, path)

        levelUrl = "http://wiki.corp.qunar.com/plugins/pagetree/naturalchildren.action?decorator=none&excerpt=false&sort=position" \
                   "&reverse=false&disableLinks=false&hasRoot=true&treeId=0&startDepth=1&pageId="\
                   "%s" % pageId

        #抓取层级,保存到指定path的index.html中
        content = Common.crawlUrl(levelUrl)

        self.parseAllLevel2(path,content)
        #print(content)
        #print("####################")
        soup = BeautifulSoup(content)


        imges = soup.find_all("img",src="/images/icons/tree_plus.gif")
        print(len(imges))
        for img in imges:
            div = img.find_next("div")
            url = img.find_next("a")["href"]
            print(url)
            id = self.commonParseTail(url)

            #判断id是否为数字,如果不是数字,则再次请求,查找pageId
            if not id.isdigit():
                notDigitUrlContent = Common.crawlUrl("http://wiki.corp.qunar.com%s" % url)
                soup = BeautifulSoup(notDigitUrlContent)
                id = soup.find("input", id="pageId")["value"]
                print("解析后的id=%s,不是数字,重新解析url=%s" % (id, url))

            self.crawlOneLevel2(id, path)


    #解析所有层级的url并抓取保存
    def parseAllLevel2(self, path, content):
        #print()
        soup = BeautifulSoup(content)
        links = soup.find_all(href=re.compile(r"/.*"))
        total = len(links).__str__()
        print("Total:" + total)

        for link in links:
            url = "http://wiki.corp.qunar.com" + link["href"]
            self.parseEveryPage2(path, url)
        return total

        #抓取每个页面
    def parseEveryPage2(self, path, url):
        print("Begin crawl URL=%s" % url)
        fileName = self.parsePageName2(url)
        content = Common.crawlUrl(url)

        soup = BeautifulSoup(content)
        try:
            name = soup.find("span",id="title-text").a.string
            fullDir = "%s%s" % (self.RootPath, path)
            fullPath = "%s/index.html" % fullDir

            Common.savePageAppend(fullPath,"<a href='"+fileName+".html'>"+name+"</a><br />\r\n")
        except:
            Common.savePageAppend("D:\\pages\\mm.log", "url保存失败,path=%s,url=%s\n" % (path, url))

        self.saveEveryPage2(path, fileName, content)
        self.saveEveryPageImges2(path, content)

        #解析尾部
    def parsePageName2(self, url):
        regMatch = re.compile("(.*)\?pageId=(\d+)").search(url)

        if regMatch:
            fileName = regMatch.groups()[1]
        else:
            #不匹配取尾部
            fileName = url[url.rfind("/") + 1:]
        return fileName

        #保存每个页面
    def saveEveryPage2(self, path, fileName, content):
        #图片去掉http前缀
        content = re.sub("<img src=\"(http://.*?)/", "<img src=\"", content)
        #图片去掉根路径的/
        content = content.replace("<img src=\"/", "<img src=\"")

        str = "<meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\">\n"\
              "<link type=\"text/css\" rel=\"stylesheet\" href=\"../../css/batch.css\">\n"\
              "<link type=\"text/css\" rel=\"stylesheet\" href=\"../../css/colors.css\">\n"\
              "<link type=\"text/css\" rel=\"stylesheet\" href=\"../../css/custom.css\">\n"\
              "<link type=\"text/css\" rel=\"stylesheet\" href=\"../../css/default-theme.css\">\n"\
              "<link type=\"text/css\" rel=\"stylesheet\" href=\"../../css/splitter.css\">\n"

        content = str + content

        Common.mkdir(self.RootPath + path)
        Common.savePage(self.RootPath + path + "/" + fileName + ".html", content)

        #保存页面所有图片
    def saveEveryPageImges2(self, path, content):
        soup = BeautifulSoup(content)
        imgs = soup.find_all("img")
        for img in imgs:
            self.saveImg(path, img["src"])


            #保存图片
    def saveImg(self, path, imgUrl):
        #print("   Save Img=%s" % imgUrl)
        #去除尾部?后内容
        cutImgUrl = imgUrl.split("?")[0]

        #判断是否是http开头
        isHttp = re.compile("^(http://.*?)(/.*)").match(cutImgUrl)
        if isHttp:
            #print("图片url是完整链接:" + cutImgUrl)
            fullImgUrl = cutImgUrl
            group = isHttp.groups()
            http = group[0]
            httpPath = group[1]
            cutImgUrl = httpPath
        else:
            #拼接完整url
            fullImgUrl = "http://wiki.corp.qunar.com" + imgUrl
        print("   Save fullImgUrl=%s" % fullImgUrl)

        #获取图片之前的所有目录
        match = re.compile("(/(.*))*/(.*)").search(cutImgUrl).groups()
        shortPath = match[1]
        imgName = match[2]

        if shortPath:
            prefixPath = self.RootPath + path + "/" + shortPath
        else:
            prefixPath = self.RootPath + path

        #中文转义
        imgNameCN = urllib.parse.unquote(imgName)
        print("   Save Img=%s" % prefixPath + "/" + imgNameCN)
        Common.saveImg(prefixPath, imgNameCN, fullImgUrl)



if __name__ == "__main__":
    wikiCrawlerMore = WikiCrawlerMore()
    rootCrawler = RootCrawler()

    #wikiCrawlerMore.crawlHomePage2('/display/flight')

    wikiCrawlerMore.crawlHomePage2('/display/searchdev')
    wikiCrawlerMore.crawlHomePage2('/display/tuanTech')
    wikiCrawlerMore.crawlHomePage2('/display/Qa')
    wikiCrawlerMore.crawlHomePage2('/display/hoteldev')



    #wikiCrawlerMore.crawlHomePage('/pages/viewpage.action?pageId=11993150')
    #wikiCrawlerMore.crawlHomePage('/pages/viewpage.action?pageId=12648469')
    #wikiCrawlerMore.crawlHomePage2('/pages/viewpage.action?pageId=11208167')

    #wikiCrawlerMore.parseEveryPage2("/display/searchdev","http://wiki.corp.qunar.com/pages/viewpage.action?pageId=49258337aaa")

