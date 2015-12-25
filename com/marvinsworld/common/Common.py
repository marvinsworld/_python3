# -*- coding: UTF-8 -*-
# -*- author: Eason -*-
# -*- date: 2014-10-21 23:25 -*-
#!/usr/bin/python
import os
import urllib3

__author__ = 'marvinsworld'

class RootCrawler():
    def __init__(self):
        super().__init__()

#抓取url全文
def crawlUrl(url):
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    content = r.data.decode("utf-8")
    return content

#保存文件
def savePage(path, content):
    #是否存在该文件
    hasFile = os.path.isfile(path)
    #不存在才保存
    if not hasFile:
        file = open(path, "w", encoding='utf-8')
        file.write(content)
        file.close()

#保存文件
def savePageAppend(path, content):
    file = open(path, "a", encoding='utf-8')
    file.write(content)
    file.close()

#创建目录
def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


#保存图片
def saveImg(path, name, url):
    #生成目录
    mkdir(path)

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
            savePageAppend("D:\\pages\\error.log", "图片保存失败,path=%s,imgUrl=%s\n" % (path, url))