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
class WikiCrawlerLeast(BaseCrawler):
    RootPath = "D:\\pages\\"

    def __init__(self):
        super().__init__()

    #解析home页面
    def crawlHomePage(self, path):
        fulluUrl = "http://wiki.corp.qunar.com%s" % path
        print(fulluUrl)
        content = Common.crawlUrl(fulluUrl)
        soup = BeautifulSoup(content)
        pageId = soup.find("input", id="pageId")["value"]
        print("Home解析后的id=%s,url=%s" % (pageId, fulluUrl))
        self.crawlAllLevel(pageId, path)


    #抓取全部层级
    def crawlAllLevel(self, pageId, path):
        #print(pageId, path)

        levelUrl = "http://wiki.corp.qunar.com/plugins/pagetree/naturalchildren.action?decorator=none&excerpt=false&sort=position&reverse=false&disableLinks=false&hasRoot=true&treeId=0&startDepth=10&pageId=" \
                   "%s" % pageId

        #抓取层级,保存到指定path的index.html中
        content = Common.crawlUrl(levelUrl)
        print(content)
        self.saveAllLevelToIndex(path, content)

    #保存全部层级
    def saveAllLevelToIndex(self, path, content):
        #print()
        #解析全部层级
        ####################################
        totalPage = self.parseAllLevel(path, content)
        ####################################

        #替换掉所有的页面链接,保留最后的数字
        content = re.sub(r"/pages/viewpage.action\?pageId=(\d+)", "\g<1>.html", content)
        #替换不是pageId这种的
        content = re.sub(r"/display/.*/(.*)\"", "\g<1>.html\"", content)
        #替换src的/
        content = content.replace("src=\"/", "src=\"")

        #增加编码
        content = "<meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\">"\
                  "共%s页面<br />%s" % (totalPage, content)

        fullDir = "%s%s" % (self.RootPath, path)
        fullPath = "%s/index.html" % fullDir

        self.saveIcon(fullDir)

        Common.mkdir(fullDir)
        Common.savePage(fullPath, content)
        print("Save Index Success.url=%s" % fullPath)


    #保存小图片
    def saveIcon(self, fullDir):
        imges = ["/images/icons/tree_square.gif", "/images/icons/tree_minus.gif",
                 "/s/1810/98/_/images/icons/docs_16.gif"]
        for img in imges:
            url = "http://wiki.corp.qunar.com%s" % img
            match = re.compile("^(/.*/)(.*)").match(img)

            if match:
                path = fullDir + match.groups()[0]
                imgName = match.groups()[1]
                Common.saveImg(path, imgName, url)
            else:
                print("Save icon Failed")


    #解析所有层级的url并抓取保存
    def parseAllLevel(self, path, content):
        #print()
        soup = BeautifulSoup(content)
        links = soup.find_all(href=re.compile(r"/.*"))
        total = len(links).__str__()
        print("Total:" + total)

        for link in links:
            url = "http://wiki.corp.qunar.com" + link["href"]
            self.parseEveryPage(path, url)
        return total


    #抓取每个页面
    def parseEveryPage(self, path, url):
        print("Begin crawl URL=%s" % url)
        fileName = self.parsePageName(url)
        content = Common.crawlUrl(url)
        self.saveEveryPage(path, fileName, content)
        self.saveEveryPageImges(path, content)


    #解析尾部
    def parsePageName(self, url):
        regMatch = re.compile("(.*)\?pageId=(\d+)").search(url)

        if regMatch:
            fileName = regMatch.groups()[1]
        else:
            #不匹配取尾部
            fileName = url[url.rfind("/") + 1:]
        return fileName


    #保存每个页面
    def saveEveryPage(self, path, fileName, content):
        #图片去掉http前缀
        content = re.sub("<img src=\"(http://.*?)/", "<img src=\"", content)
        #图片去掉根路径的/
        content = content.replace("<img src=\"/", "<img src=\"")

        str = "<meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\">\n" \
              "<link type=\"text/css\" rel=\"stylesheet\" href=\"../../css/batch.css\">\n" \
              "<link type=\"text/css\" rel=\"stylesheet\" href=\"../../css/colors.css\">\n" \
              "<link type=\"text/css\" rel=\"stylesheet\" href=\"../../css/custom.css\">\n" \
              "<link type=\"text/css\" rel=\"stylesheet\" href=\"../../css/default-theme.css\">\n" \
              "<link type=\"text/css\" rel=\"stylesheet\" href=\"../../css/splitter.css\">\n"

        content = str + content

        Common.mkdir(self.RootPath + path)
        Common.savePage(self.RootPath + path + "/" + fileName + ".html", content)


    #保存页面所有图片
    def saveEveryPageImges(self, path, content):
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

    #抓取所有url
    def crawlHomeLinks(self,homeUrls):
        for homeUrl in homeUrls:
            self.crawlHomePage(homeUrl)
            Common.savePageAppend("D:\\pages\\complete.log", homeUrl+"\n")
            print("#################################################################")


if __name__ == "__main__":
    crawler = WikiCrawlerLeast()
    rootCrawler = RootCrawler()
#    homeUrls = rootCrawler.getHomeLink("http://wiki.corp.qunar.com/dashboard.action")
#    print(homeUrls)

    homeUrls = [
        #'/display/CallCenter', '/display/CM',
        #        '/display/corpux', '/display/mysql', '/display/devwiki',
        #        '/display/HRBP', '/display/opswiki', '/display/QBOSS', '/display/workflow', '/display/DevelopmentProcess',
        #        '/display/publicsystem', '/display/fe', '/display/tuan', '/display/teambuilding', '/display/inter',
        #        '/display/operation', '/display/packagetts', '/display/packdev', '/display/vacationFE', '/display/dujiaCC',
                '/display/searchdev',
        # '/display/searchsem', '/display/qadsoperator', '/display/traveltuan', '/display/package',
        #        '/display/DujiaDev', '/display/travel', '/display/mobilepay', '/display/tsxm', '/display/tradesc',
        #        '/display/fic',
         '/display/flight',
        # , '/display/Settlement', '/display/mddyych', '/display/mudidishanhuyunyin',
        #        '/display/desmarket',
        '/display/tuanTech',
        '/display/Qa',
        #'/display/gcgjz',
        #        '/display/CPC',
        #        '/display/HOTELUED',
        #        '/display/jiudianzhicheng', '/display/hoteltuijin', '/display/hotelpm',
        '/display/hoteldev'#,
        #        '/display/newstaff'
        ]
    #crawler.crawlHomeLinks(homeUrls)

    ##抓取单一模块
    #crawler.crawlHomePage("/display/searchdev")

    #抓取一个页面,修改css
    #crawler.parseEveryPage("/display/mobilepay","http://wiki.corp.qunar.com/display/mobilepay/1.+Findbugs")