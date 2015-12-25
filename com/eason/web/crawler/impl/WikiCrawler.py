# -*- coding: UTF-8 -*-
# -*- author: Eason -*-
# -*- date: 2014-10-21 23:25 -*-
#!/usr/bin/python
import codecs
import io
import os
import re
from bs4 import BeautifulSoup
import urllib3
import urllib.parse
from com.eason.web.crawler.BaseCrawler import BaseCrawler

#搜索结果抓取
class WikiCrawler(BaseCrawler):
    RootPath = "E:\\pages\\"

    def __init__(self):
        super().__init__()

    #抓取url全文
    def crawlUrl(self, url):
        http = urllib3.PoolManager()
        r = http.request('GET', url)
        content = r.data.decode("utf-8")
        return content

    #解析尾部
    def commonParseTail(self, url):
        regMatch = re.compile("(.*)\?pageId=(\d+)").search(url)

        if regMatch:
            id = regMatch.groups()[1]
        else:
            #不匹配取尾部
            id = url[url.rfind("/") + 1:]
        return id


    #解析一级节点的pageId,如果没有则获取末尾内容
    def parseFirstNodes(self, content):
        #print(content)
        soup = BeautifulSoup(content)
        firstNodes = soup.find("div", id="page-children")
        #print(firstNodes)

        arr = []
        for idx, val in enumerate(firstNodes.find_all("a")):
            #一级节点的url
            href = val["href"]
            title = val.text
            title = val.text

            #原id,可能不为数字
            id = self.commonParseTail(href)
            firstUrl = "<a class=\"first\" href=\"%s.html\">%s</a>" % (id, title)

            #保存根结点文件
            fistNodeContent = self.crawlUrl("http://wiki.corp.qunar.com%s" % href)
            self.savePage(href, fistNodeContent)

            #判断id是否为数字,如果不是数字,则再次请求,查找pageId
            if not id.isdigit():
                notDigitUrlContent = self.crawlUrl("http://wiki.corp.qunar.com%s" % href)
                soup = BeautifulSoup(notDigitUrlContent)
                id = soup.find("input", id="pageId")["value"]
                print("解析后的id=%s,不是数字,重新解析url=%s" % (id, href))

            url = "http://wiki.corp.qunar.com/plugins/pagetree/naturalchildren.action?decorator=none&excerpt=false&sort=position&reverse=false&disableLinks=false&hasRoot=true&treeId=0&startDepth=10&pageId="
            url += id

            print(url)

            self.saveIndex(url, firstUrl,idx)
            arr.append(url)
        return arr

    #保存根结点的内容到首页
    def saveIndex(self, url, title,index):
        #抓取根结点url
        content = self.crawlUrl(url)
        #替换掉所有的页面链接,保留最后的数字
        content = re.sub(r"/pages/viewpage.action\?pageId=(\d+)", "\g<1>.html", content)
        #替换src的/
        content = content.replace("src=\"/", "src=\"")

        #以追加方式保存文件
        file = open("%sindex.html" % self.RootPath, "a", encoding='utf-8')
        if index==0:
            file.write("<meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\">")
        file.write(title + "<br />")
        file.write(content)

    #保存小图片
    def saveIcon(self):
        imges = ["/images/icons/tree_square.gif","/images/icons/tree_minus.gif","/s/1810/98/_/images/icons/docs_16.gif"]
        for img in imges:
            self.saveImg(img)


    #解析所有一级一下节点的链接
    def parseNextNodes(self, url):
        #print(url)
        #url = "http://wiki.corp.qunar.com/plugins/pagetree/naturalchildren.action?decorator=none&excerpt=false&sort=position&reverse=false&disableLinks=false&hasRoot=true&treeId=0&startDepth=10&pageId=63243065"
        content = self.crawlUrl(url)
        #print(content)
        soup = BeautifulSoup(content)
        links = soup.find_all(href=re.compile(r"/.*"))
        #print(links)

        urls = []
        for link in links:
            #print(link["href"])
            url = "http://wiki.corp.qunar.com" + link["href"]
            urls.append(url)

        return urls


    #解析每个页面,保存页面,保存图片
    def parsePageContent(self, url):
        print(url)
        content = self.crawlUrl(url)
        self.savePage(url, content)
        soup = BeautifulSoup(content)

        imgs = soup.find_all("img")
        for img in imgs:
            self.saveImg(img["src"])

    #保存页面
    def savePage(self, url, content):
        content = re.sub("<img src=\"(http://.*?)/", "<img src=\"", content)

        content = content.replace("<img src=\"/", "<img src=\"")
        name = self.commonParseTail(url)

        #是否存在该文件
        hasFile = os.path.isfile(self.RootPath + name + ".html")
        #不存在才保存
        if not hasFile:
            file = open(self.RootPath + name + ".html", "w", encoding='utf-8')
            file.write(content)
            file.close()

    #保存图片
    def saveImg(self, imgUrl):
        #print(imgUrl)

        #去除尾部?后内容
        cutImgUrl = imgUrl.split("?")[0]
        #print(cutImgUrl)

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

        #print(cutImgUrl)

        #获取图片之前的所有目录
        match = re.compile("(/(.*))*/(.*)").search(cutImgUrl).groups()
        path = match[1]
        imgName = match[2]

        imgNameCN = urllib.parse.unquote(imgName)
        #        print(imgNameCN)
        #        print(path)

        if path:
            prefixPath = self.RootPath + path
        else:
            prefixPath = self.RootPath

        #生成目录
        if not os.path.exists(prefixPath):
            os.makedirs(prefixPath)

        http = urllib3.PoolManager()
        try:
            data = http.request("GET", fullImgUrl).data
            file = open(prefixPath + "/" + imgNameCN, "wb")
            file.write(data)
            file.close()
        except:
            print("图片请求失败,fullImgUrl=" + fullImgUrl)
        #        print(data)

        return imgNameCN


if __name__ == "__main__":
    crawler = WikiCrawler()

    #抓取根页面内容
    #工程师wiki
    content = crawler.crawlUrl("http://wiki.corp.qunar.com/pages/viewpage.action?pageId=63243093")
    #机票开发组
    #content = crawler.crawlUrl("http://wiki.corp.qunar.com/pages/viewpage.action?pageId=1048777")
    #content = crawler.crawlUrl("http://wiki.corp.qunar.com/display/flight/Code+Review")

    print("开始解析一级节点...")
    firstNodes = crawler.parseFirstNodes(content)
    crawler.saveIcon()

    #-----------------------

    #    print("开始遍历一级节点...")
    #    pageUrls = []
    #    for tag in firstNodes:
    #        urlArr = crawler.parseNextNodes(tag)
    #        #print(url)
    #        for url in urlArr:
    #            crawler.parsePageContent(url)



    #
    #        #pageUrls.append(urlArr)
    #
    #
    #    print("开始抓取页面...")

    #    for urlArr in pageUrls:
    #        for url in urlArr:
    #            crawler.parsePageContent(url)



    #crawler.parseNextNodes("aa")
    #crawler.parsePageContent("http://wiki.corp.qunar.com/pages/viewpage.action?pageId=63243010")
    #crawler.parsePageContent("http://wiki.corp.qunar.com/display/devwiki/Silk+Icons")
    #crawler.parsePageContent("http://wiki.corp.qunar.com/pages/viewpage.action?pageId=63243020")


    #    crawler.saveImg("/download/attachments/81035891/4.PNG")
    #    crawler.saveImg("http://source.qunar.com/common/silk/accept.png")

    #    print(urllib.parse.unquote("%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7+2014-11-20+%E4%B8%8B%E5%8D%883.45.19.png"))
    #    print(urllib.parse.unquote("aaaaaaaaa.png"))

    #    str = "<img src=\"http://source.qunar.com/common/silk/page_white_swoosh.png\" style=\"border: 0px solid black\" />"
    #
    #    print(str.replace("<img src=\"/http://(.*?)/.*", "<img src=\""))
    #
    #    print(re.sub("<img src=\"(http://.*?)/", "<img src=\"",str))

    #    str = "/download/attachments/131074/global.logo"
    #    str1 = "/a.jpg"
    #
    #    match = re.compile("(/(.*))*/(.*)").search(str1).groups()
    #    path = match[0]
    #    imgName = match[1]
    #
    #
    #    print(path)
    #    print(imgName)
    #    print(match[2])

    #一级节点的url
    #    href = "/display/flight/Code+Review"
    #
    #    id = crawler.commonParseTail(href)
    #    print(id)
    #
    #    url = "http://wiki.corp.qunar.com/plugins/pagetree/naturalchildren.action?decorator=none&excerpt=false&sort=position&reverse=false&disableLinks=false&hasRoot=true&treeId=0&startDepth=10&pageId="
    #    if id == "TC+DEV":
    #        url += "63243027"
    #    else:
    #        url += id
    #
    #    print(url)
    #arr.append(url)

    #    content ="<img src=\"/s/1810/98/_/images/icons/docs_16.gif\" height=\"16\" width=\"16\" border=\"0\" align=\"absmiddle\" title=\"BDS开关监控接口\"><a href='/pages/viewpage.action?pageId=64784191'>BDS开关监控接口</a>"
    ##
    ##    match = re.compile("/pages/viewpage.action?pageId=(\d+)").search(content).groups()
    ##    print(match[0])
    #
    #    regMatch = re.compile("(.*)\?pageId=(\d+)").search(content)
    #
    #    print(regMatch.groups()[1])
    #
    #    content = re.sub(r"/pages/viewpage.action\?pageId=(\d+)", "\g<1>.html",content)
    #
    #    content = re.sub("<img src=\"(http://.*?)/", "<img src=\"",content)
    #
    #    content = content.replace("<a href=\"/pages/viewpage.action?pageId=", "<a href=\"")
    #    print(content)