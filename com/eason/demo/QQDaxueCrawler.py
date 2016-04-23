#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -*- author: Eason -*-
# -*- date: 2016-04-23 17:50 -*-

# QQ大学视频抓取
import re


class QQDaxueCrawler:
    def __init__(self):
        pass

    # 读取文件
    def crawl(self, filename):
        result = []

        file = open("/home/eason/javawork/_python3/crawler/data/video_cache_2")
        lines = file.readlines()
        for line in lines:
            if self.parse(line):
                result.append(line)
            else:
                continue

        return result

    # 解析出.mp4?
    def parse(self, txt):
        return re.search(r'mp4', txt)

    # 组装数据
    def build(self, txt):
        print(txt)

    # 输出
    def display(self, lines):
        for line in lines:
            print(line)


if __name__ == '__main__':
    crawler = QQDaxueCrawler()
    res = crawler.crawl("")
    print(res.__len__())
    crawler.display(res)
