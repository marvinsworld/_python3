# -*- coding: UTF-8 -*-
# -*- author: Eason -*-
# -*- date: 2015-12-19 18:07 -*-
#!/usr/bin/python

from selenium import webdriver
import selenium.webdriver.common.keys
import selenium.webdriver.chrome.webdriver

class SelenuimDemo():
    def __init__(self):
        super().__init__()



    ##1.获取ip代理池
    ##2.使用代理模拟
    ##3.请求链接


if __name__=="__main__":
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument("--proxy-server=39.78.235.191git :8888")

    driver = webdriver.Chrome(
        executable_path="/usr/local/bin/chromedriver",
        chrome_options=chrome_option)
    driver.get('http://www.baidu.com')
    print(driver.title)

#    driver.get("http://www.python.org")
#    assert "Python" in driver.title
#    elem = driver.find_element_by_name("q")
#    elem.send_keys("pycon")
#    elem.send_keys(selenium.webdriver.common.keys.Keys.RETURN)
#    assert "No results found." not in driver.page_source
#    driver.close()
#
#    selenium.webdriver.chrome.webdriver.WebDriver()
#    http://quloushang.com/?fromuid=14611
