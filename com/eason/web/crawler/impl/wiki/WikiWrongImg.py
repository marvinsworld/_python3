# -*- coding: UTF-8 -*-
# -*- author: Eason -*-
# -*- date: 2015-07-17 01:31 -*-
#!/usr/bin/python
import os
import re
import urllib.parse
import urllib3
import com.eason.web.crawler.BaseCrawler
from com.marvinsworld.common import Common

class WikiWrongImg(com.eason.web.crawler.BaseCrawler.BaseCrawler):
    RootPath = "F:\\pages\\"

    def __init__(self):
        super().__init__()


    def parseLine(self, line):
        if line != "":
            path = re.split(r",", line)[1][5:]
            url = re.split(r",", line)[2][7:]
            print(path)
            print(url)

            httpUrl = re.compile("^(http.*/)(.*)").match(url).groups()[0]
            imgName = re.compile("^(http.*/)(.*)").match(url).groups()[1]
            #print("---"+httpUrl)

            url = httpUrl + urllib.parse.quote(imgName)

            self.saveImg(path, imgName, url)


            #保存图片
    def saveImg(self,path, name, url):
        #生成目录
        Common.mkdir(path)

        fullPath = path + "/" + name
        #是否存在该文件
        hasFile = os.path.isfile(fullPath)
        #不存在才保存
        if not hasFile:
            http = urllib3.PoolManager()
            try:
                data = http.request("GET", url).data
                file = open(fullPath, "wb")
                file.write(data)
                file.close()
            except:
                print("图片保存失败,imgUrl=%s" % url)
                #savePageAppend("D:\\pages\\error.log", "图片保存失败,path=%s,imgUrl=%s\n" % (path, url))



if __name__ == "__main__":
    crawler = WikiWrongImg()
    file = open("D:\pages\error.log", "r", encoding='utf-8')
    while 1:
        line = file.readline()
        #print(line)
        crawler.parseLine(line)
        if not line:
            break

