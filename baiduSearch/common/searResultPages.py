__author__ = 'tixie'

from baiduSearch.common.searchEngines import SearchEngines


class SearResultPages:
    totalPage = 0
    keyword = None,
    searchEngineUrl = None
    currentPage = 0
    searchEngine = None

    def __init__(self, keyword, search_engine, total_page):
        self.searchEngine = search_engine.lower()
        self.searchEngineUrl = SearchEngines[self.searchEngine]
        self.totalPage = total_page
        self.keyword = keyword
        print("total page:{0}".format(self.totalPage))

    def __iter__(self):
        return self

    def current_url(self, currentPage):
        # return self.searchEngineUrl.format(self.keyword, str(self.currentPage * 10))
        se_page = self.searchEngineUrl.format(self.keyword, str(self.currentPage * 10))
        return se_page

    def next(self):
        while self.currentPage < self.totalPage:
            url = self.current_url(self.currentPage)
            # self.currentPage = self.currentPage + 1
            self.currentPage += 1
            print("组装搜索页:::", url)
            print("下一搜索页号:::", self.currentPage)
            yield url
        # raise StopIteration
