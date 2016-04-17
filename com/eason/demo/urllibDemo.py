# -*- coding: UTF-8 -*-
# -*- author: Eason -*-
# -*- date: 2015-12-22 22:38 -*-
#!/usr/bin/python
import urllib.request


class urllibDemo():
    def __init__(self):
        super().__init__()

    def proxy(self):
        proxyIp = "27.191.234.69:9999"
        # 添加代理
        proxy_handler = urllib.request.ProxyHandler({'http': proxyIp});
        proxy_auth_handler = urllib.request.ProxyBasicAuthHandler();
        opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler);

        userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'


        # 添加头信息
        opener.addheaders = [
            ('User-Agent', userAgent)
        ]

        response = opener.open('http://quloushang.com/?fromuid=14611')

    def opern(self):
        url = "http://www.baidu.com"

        headers = {
            # 'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'  #,
            #'Accept-Encoding':'gzip'#,
            #                   'Connection':'close',
            #                   'Referer':None #注意如果依然不能抓取的话，这里可以设置抓取网站的host
        }

        opener = urllib.request.build_opener()
        opener.addheaders('Accept', 'text/html;q=0.9,*/*;q=0.8')

        # opener.addheaders = [headers]
        data = opener.open(url).read()

        print(data)

    def proxyurl(self):
        proxy_support = urllib.request.ProxyHandler({'http': 'http://117.177.250.146:80'})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)

        # urllib.request.urlretrieve("http://quloushang.com/?fromuid=14611")


        a = urllib.request.urlopen("http://quloushang.com/?fromuid=14611").read().decode("gbk")

# print(a)


if __name__ == "__main__":
    demo = urllibDemo()
    demo.proxyurl()

