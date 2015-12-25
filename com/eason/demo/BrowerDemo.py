from splinter.browser import Browser


class BrowserDemo():
    def test(self):
        print("11")

if __name__ == "__main__":
    b = Browser(driver_name="chrome")
    b.visit("http://www.baidu.com")  ###注意不要去掉http://

    b.fill('wd', '国庆是猪')
    button = b.find_by_id('su')

    button.click()