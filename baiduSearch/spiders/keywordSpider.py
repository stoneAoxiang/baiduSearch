import csv
import re
import time

from scrapy import Request
from scrapy.selector import Selector
from scrapy.spiders import Spider
from w3lib.html import remove_tags

from baiduSearch.common.searResultPages import SearResultPages
from baiduSearch.common.searchEngines import SearchEngineResultSelectors


class KeywordSpider(Spider):
    name = 'keywordSpider'
    allowed_domains = ['bing.com', 'google.com', 'baidu.com']
    start_urls = []
    keyword = None
    searchEngine = None
    writerFile = None
    page_urls = None

    # def __init__(self, keyword, se='baidu', pages=1, *args, **kwargs):
    def __init__(self, se='baidu', pages=1, *args, **kwargs):
        super(KeywordSpider, self).__init__(*args, **kwargs)
        # self.keyword = keyword.lower()
        self.searchEngine = se.lower()
        self.selector = SearchEngineResultSelectors[self.searchEngine]

        for word in open("keyword.txt", encoding="utf-8"):
            self.keyword = word
            self.page_urls = SearResultPages(self.keyword, se, int(pages)).next()

        # page_urls = SearResultPages(keyword, se, int(pages)).next()

        self.writerFile = csv.writer(open("scrapy_result.csv", "w", encoding="UTF8", newline=""), delimiter=";")
        data = ["url", "query", "title", "content", "scrapy_time"]
        self.writerFile.writerow(data)

        for url in self.page_urls:
            print(url)
            self.start_urls.append(url)

    def parse(self, response):
        # print("解析请求的URL:::", response.url)
        for url in Selector(response).xpath(self.selector).getall():
            # print("列表项URL:::", url)
            yield Request(url, callback=self.detail_parse, dont_filter=True)

    def detail_parse(self, response):
        title = response.css("title::text")
        # print("详情页的TITLE:::", response.css("title::text"))
        div_count = len(response.css("div").getall())
        # print("div_count:::", div_count)
        len_list = []
        content_list = []
        for content in response.css("div").getall():
            process = re.sub(r'[\t\r\n\s]', '', remove_tags(content))
            # if len(process) > 500:
            #     select_content = process
            len_list.append(len(process))
            content_list.append(process)

        max_len = max(len_list)
        match_index = len_list.index(max_len)
        # print("div最大长度:::", max_len)
        # print("div最大长度匹配位置:::", match_index)

        match_content = content_list[match_index]
        match_content = re.sub(r'<script.*?>[\s\S]*?<\/script>', "", match_content)
        match_content = re.sub(r'<style.*?>([\s\S]*?)</style>', "", match_content)
        match_content = re.sub(r'{[\s\S]*}', "", match_content)
        match_content = re.sub(r'<!--.*?-->', "", match_content)
        match_content = re.sub(r'<p[^>]*?>', '<p>', match_content)
        match_content = re.sub(r'[\t\r\f\v]', '', match_content)

        data = [response.url, self.keyword, title, match_content, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())]
        self.writerFile.writerow(data)

        # print("详情页的内容:::      ", match_content)
        #
        # print()
        # print()
        # print()


