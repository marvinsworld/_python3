import os
import re

__author__ = 'zhiqiang.ge'


#截取路径
def spiltPath(self, shortUrl):
    match = re.compile("(/(.*))*/(.*)").search(shortUrl).groups()
    path = match[0]
    prefixPath = self.RootPath + path
    #fileName = match[2]
    #print(path)
    #print(fileName)
    #生成目录
    if not os.path.exists(prefixPath):
        os.makedirs(prefixPath)
