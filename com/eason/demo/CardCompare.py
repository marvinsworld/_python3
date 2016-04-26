# -*- coding: UTF-8 -*-
# -*- author: Eason -*-
# -*- date: 2015-12-22 22:38 -*-
# !/usr/bin/python
import re


class CardCompare():
    def crawler(self):
        result = []

        file = open("D:/javawork/_python3/crawler/data/wellet.log", encoding="utf-8")
        lines = file.readlines()
        for line in lines:
            if re.search(r'实时调用物美查询美通卡接口\,卡面号CardFaceChk', line):
                result.append(line)
            else:
                continue

        return result

    def compare(self):
        result = self.crawler()
        for line in result:
            regmatch = re.compile(r'(\d{2}:\d{2}:\d{2}\.\d{3}).*?CardFaceChk (\d*).*?cardFaceNo\":\"(\d+)').search(line)
            # .*?cardFaceNo\":\"(\d+)
            if regmatch:
                time = regmatch.groups()[0]
                cardface = regmatch.groups()[1]
                cardfacea = regmatch.groups()[2]

                if cardface != cardfacea:
                    print(time + "--" + cardface + "---" + cardfacea)


if __name__ == '__main__':
    cardObj = CardCompare()
    cardObj.compare()
