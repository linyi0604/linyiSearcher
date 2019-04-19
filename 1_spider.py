import requests
from lxml import etree
import random
import COMMON
import os
from selenium import webdriver
import pandas as pd
"""
这里是建立搜索引擎的第一步
"""


class Spider_BaiduTieba(object):

    def __init__(self):
        self.start_url = "/f/index/forumpark?pcn=娱乐明星&pci=0&ct=1&rn=20&pn=1"
        self.base_url = "http://tieba.baidu.com"
        self.headers = COMMON.HEADERS
        self.driver = webdriver.Chrome()
        self.urlset = set()
        self.titleset = set()

    def get(self, url):
        header = random.choice(self.headers)
        response = requests.get(url=url, headers=header, timeout=10)
        return response.content

    def parse_url(self, url):
        """通过url 拿到xpath对象"""
        print(url)
        header = random.choice(self.headers)
        response = requests.get(url=url, headers=header, timeout=10)
        # 如果获取的状态码不是200 则抛出异常
        assert response.status_code == 200
        xhtml = etree.HTML(response.content)
        return xhtml

    def get_base_url_list(self):
        """获得第一层url列表"""
        if os.path.exists(COMMON.BASE_URL_LIST_FILE):
            li = self.read_base_url_list()
            return li
        next_page = [self.start_url]
        url_list = []
        while next_page:
            next_page = next_page[0]
            xhtml = self.parse_url(self.base_url + next_page)
            tmp_list = xhtml.xpath('//div[@id="ba_list"]/div/a/@href')
            url_list += tmp_list
            next_page = xhtml.xpath('//div[@class="pagination"]/a[@class="next"]/@href')
            print(next_page)
        self.save_base_url_list(url_list)
        return url_list

    def save_base_url_list(self, base_url_list):
        with open(COMMON.BASE_URL_LIST_FILE, "w") as f:
            for u in base_url_list:
                f.write(self.base_url + u + "\n")

    def read_base_url_list(self):
        with open(COMMON.BASE_URL_LIST_FILE, "r") as f:
            line = f.readlines()
        li = [s.strip() for s in line]
        return li

    def driver_get(self, url):
        try:
            self.driver.set_script_timeout(5)
            self.driver.get(url)
        except:
            self.driver_get(url)
    def run(self):
        """爬虫程序入口"""
        # 爬取根网页地址
        base_url_list = self.get_base_url_list()
        data_list = []
        for url in base_url_list:
            self.driver_get(url)
            html = self.driver.page_source
            xhtml = etree.HTML(html)
            a_list = xhtml.xpath('//ul[@id="thread_list"]//a[@rel="noreferrer"]')
            for a in a_list:
                title = a.xpath(".//@title")
                url = a.xpath(".//@href")
                if not url or not title or title[0]=="点击隐藏本贴":
                    continue
                url = self.base_url + url[0]
                title = title[0]

                if url in self.urlset:
                    continue

                data_list.append([title, url])
                self.urlset.add(url)
                data = pd.DataFrame(data_list, columns=["title,", "url"])
                data.to_csv("./data/database.csv")




if __name__ == '__main__':
    s = Spider_BaiduTieba()
    s.run()