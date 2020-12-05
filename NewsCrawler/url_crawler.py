from time import sleep
from bs4 import BeautifulSoup
from multiprocessing import Process
from NewsCrawler.exceptions import *
from NewsCrawler.articleparser import ArticleParser
from NewsCrawler.writer import Writer
import os
import platform
import calendar
import requests
import re
from typing import List, Dict


class UrlCrawler(object):

    def __init__(self):
        self.categories = {'정치': 100, '경제': 101, '사회': 102, '생활문화': 103, '세계': 104, 'IT과학': 105, '오피니언': 110,
                           'politics': 100, 'economy': 101, 'society': 102, 'living_culture': 103, 'world': 104,
                           'IT_science': 105, 'opinion': 110}
        self.selected_categories = []
        self.date = {'start_month': 0, 'start_day': 0, 'end_month': 0, 'end_day': 0}
        self.user_operating_system = str(platform.system())
        self.headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)\
                                        # AppleWebKit/537.36 (KHTML, like Gecko)\
                                         Chrome/63.0.3239.132 Safari/537.36',
                        "Accept": "text/html",
                        "Pragma": "no-cache",
                        "Cache-Control": "no-cache"}

    def set_category(self, *args: List[str]):
        """ 한글로 받은 카테고리를 고유번호로 매핑 """
        for key in args:
            if self.categories.get(key) is None:
                raise InvalidCategory(key)
        self.selected_categories = args
        print(self.selected_categories)

    def set_date_range(self, start_month: int, start_day: int, end_month: int, end_day: int):
        """ 주어진 날짜 범위가 유효한지 판단하고, self.date 형태로 내보낸다."""
        args = [start_month, start_day, end_month, end_day]

        if start_month < 1 or start_month > 12:
            raise InvalidMonth(start_month)
        if end_month < 1 or end_month > 12:
            raise InvalidMonth(end_month)
        if start_month == end_month and start_day > end_day:
            raise OverbalanceMonth(start_month, end_month)
        for key, date in zip(self.date, args):
            self.date[key] = date
        print(self.date)

    def make_news_page_url(self, category_url: str, start_month, start_day, end_month, end_day) -> List[str]:
        made_urls = []
        print("making news_page_url start")
        for month in range(start_month, end_month + 1):
            if start_month == end_month:
                month_startday = start_day
                month_endday = end_day
            else:
                if month == start_month:
                    month_startday = start_day
                    month_endday = calendar.monthrange(2020, month)[1]  # 해당 월의 말일
                elif month == end_month:
                    month_startday = 1
                    month_endday = end_day
                else:
                    month_startday = 1
                    month_endday = calendar.monthrange(2020, month)[1]

            for day in range(month_startday, month_endday + 1):
                if len(str(month)) == 1:
                    month = "0" + str(month)
                if len(str(day)) == 1:
                    day = "0" + str(day)

                # 날짜별로 Page Url 생성
                url = category_url + '2020' + str(month) + str(day)
                # totalpage는 네이버 페이지 구조를 이용해서 page=10000으로 지정해 totalpage를 알아냄
                # page=10000을 입력할 경우 페이지가 존재하지 않기 때문에 page=totalpage로 이동 됨 (Redirect)
                totalpage = self.find_news_totalpage(url + "&page=10000")
                sleep(0.02)
                for page in range(1, totalpage + 1):
                    made_urls.append(url + "&page=" + str(page))

        print('made_urls:', len(made_urls))
        return made_urls

    def find_news_totalpage(self, url: str) -> int:
        # 당일 기사 목록 페이지 수를 반환
        try:
            totalpage_url = url
            request_content = requests.get(totalpage_url, headers=self.headers)
            document_content = BeautifulSoup(request_content.content, 'html.parser')
            headline_tag = document_content.find('div', {'class': 'paging'}).find('strong')
            regex = re.compile(r'<strong>(?P<num>\d+)')
            match = regex.findall(str(headline_tag))
            return int(match[0])
        except Exception as e:
            print(e)
            return 0

    def get_url_data(self, url: str, max_tries=10):
        remaining_tries = int(max_tries)

        while remaining_tries > 0:
            try:
                return requests.get(url, headers=self.headers)
            except requests.exceptions:
                sleep(60)
            remaining_tries = remaining_tries - 1
        raise ResponseTimeout()

    def url_crawling(self, category_name: str):
        # Multi Process PID
        print(category_name + " PID: " + str(os.getpid()))

        # 기사 URL 형식
        url = "http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=" + str(
            self.categories.get(category_name)) + "&date="

        # 2020년 start_month월 ~ end_month 날짜까지 기사를 수집합니다.
        day_urls = self.make_news_page_url(url, self.date['start_month'], self.date['start_day'],
                                           self.date['end_month'], self.date['end_day'])
        print(category_name + " Urls are generated")
        # day_urls: 카테+날짜(day)를 포함한 url로, 이 안에서 크롤링 대상이 될 url을 가져온다.

        count = 0
        news_metadata = []
        batch_size = 1000  # db 연결 회수를 줄이기 위해 batchsize를 지정하여 1000개씩 insert
        for URL in day_urls:

            regex = re.compile("date=(\d+)")
            news_date = regex.findall(URL)[0]

            request = self.get_url_data(URL)

            document = BeautifulSoup(request.content, 'html.parser')

            # html - newsflash_body - type06_headline, type06
            # 각 페이지에 있는 기사들 가져오기
            post_temp = document.select('.newsflash_body .type06_headline li dl')
            post_temp.extend(document.select('.newsflash_body .type06 li dl'))

            # 각 페이지에 있는 기사들의 url 저장
            for line in post_temp:
                metadata = {}
                # https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=100&oid=056&aid=0010424247 이런애들
                _url = line.a.get('href')  # 해당되는 page에서 모든 기사들의 URL을 post 리스트에 넣음
                metadata = ArticleParser.create_metadata(URL, _url)
                news_metadata.append(metadata)

            del post_temp

            if len(news_metadata) >= batch_size:
                try:
                    Writer.insert_values_to_db('news_metadata_temp', news_metadata)
                    count += len(news_metadata)
                    news_metadata = []
                except Exception as e:
                    print(e, '\n' + category_name + " PID: " + str(os.getpid()) + " Date: " +
                          URL.split('&')[-2].split('=')[1] + "Is FAILED")
            else:
                continue

        if len(news_metadata) > 0:
            try:
                Writer.insert_values_to_db('news_metadata_temp', news_metadata)
                count += len(news_metadata)
                news_metadata = []
            except Exception as e:
                print(e, '\n' + category_name + " PID: " + str(os.getpid()) + " Date: " +
                      URL.split('&')[-2].split('=')[1] + "Is FAILED")

        print(f"Done: {category_name} PID: {str(os.getpid())} /{count} url")

    def start(self):
        # MultiProcess 크롤링 시작
        # 카테고리별로 한 프로세스
        procs = []
        for category_name in self.selected_categories:
            proc = Process(target=self.url_crawling, args=(category_name,))
            procs.append(proc)
            proc.start()
        for proc in procs:
            proc.join()



if __name__ == "__main__":
    categories = {'정치': 100, '경제': 101, '사회': 102, '생활문화': 103, '세계': 104, 'IT과학': 105, '오피니언': 110}
    keys = list(categories.keys())
    Crawler = UrlCrawler()

    Crawler.set_category(keys[0], keys[1], keys[2], keys[3], keys[4], keys[5])
    Crawler.set_date_range(9, 1, 9, 30)
    Crawler.start()
