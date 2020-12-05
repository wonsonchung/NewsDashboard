from time import sleep
from bs4 import BeautifulSoup
from multiprocessing import Process
from NewsCrawler.exceptions import *
from NewsCrawler.articleparser import ArticleParser
from NewsCrawler.writer import Writer
import os
import platform
import requests
from typing import List, Dict
import random
import string


class ArticleCrawler(object):
    def __init__(self, start_date: str, end_date: str):
        self.categories = {'정치': 100, '경제': 101, '사회': 102, '생활문화': 103, '세계': 104, 'IT과학': 105, '오피니언': 110,
                           'politics': 100, 'economy': 101, 'society': 102, 'living_culture': 103, 'world': 104,
                           'IT_science': 105, 'opinion': 110}
        self.selected_categories = []
        self.start_date = start_date
        self.end_date = end_date
        self.user_operating_system = str(platform.system())
        self.headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)\
                                        # AppleWebKit/537.36 (KHTML, like Gecko)\
                                         Chrome/63.0.3239.132 Safari/537.36',
                        "Accept": "text/html",
                        "Pragma": "no-cache",
                        "Cache-Control": "no-cache"}
        self.done_aid = []

    def set_category(self, *args: List[str]):
        """ 한글로 받은 카테고리를 고유번호로 매핑 """
        for key in args:
            if self.categories.get(key) is None:
                raise InvalidCategory(key)
        self.selected_categories = args
        print(self.selected_categories)

    def crawling(self, category_name):
        # Multi Process PID
        print(category_name + " PID: " + str(os.getpid()))

        # 크롤링 대상이 될 뉴스를 [[카테고리번호, aid, url]]로 불러온다.
        crawling_targets = Writer.get_url_to_crawl(self.categories[category_name], self.start_date, self.end_date)
        print(f"Start: {category_name}, {self.start_date} ~ {self.end_date} has {len(crawling_targets)} urls")
        delimiter = ''.join(random.choices(string.digits, k=4))

        batch_size = 1000  # 10000개씩 쪼개서 s3에 넣자
        i = 0
        failed_urls = []  # 실패한 기사들은 다시 시도할 수 있게 따로 db에 써두자
        failed_count = 0
        for i in range(int(len(crawling_targets) / batch_size) + 1):
            batch = {}
            for target in crawling_targets[i * batch_size:(i + 1) * batch_size]:
                category = target[0]
                aid = target[1]
                url = target[2]
                sleep(0.01)
                # 기사 HTML 가져옴
                request_content = self.get_url_data(url)
                try:
                    document_content = BeautifulSoup(request_content.content, 'html.parser')
                except Exception as e:
                    print(f"crawling failed for url:{url}, Error: {e}")
                    continue

                try:
                    # 기사 제목 가져옴
                    tag_headline = document_content.find_all('h3', {'id': 'articleTitle'}, {'class': 'tts_head'})
                    text_headline = ''  # 뉴스 기사 제목 초기화
                    # 기사  제목 예시 : [<h3 id="articleTitle">]제목내용</h3>]
                    # 필요 없는 내용 날리고 깔끔하게 처리해주기
                    text_headline = text_headline + ArticleParser.clear_headline(
                        str(tag_headline[0].find_all(text=True)))
                    if not text_headline:  # 공백일 경우 기사 제외 처리
                        continue

                    # 기사 본문 가져옴
                    tag_content = document_content.find_all('div', {'id': 'articleBodyContents'})
                    text_sentence = ''  # 뉴스 기사 본문 초기화
                    text_sentence = text_sentence + ArticleParser.clear_content(str(tag_content[0].find_all(text=True)))
                    if not text_sentence:  # 공백일 경우 기사 제외 처리
                        continue

                    # 기사 언론사 가져옴(공백 허용)
                    tag_company = document_content.find_all('meta', {'property': 'me2:category1'})
                    text_company = ''  # 언론사 초기화
                    text_company = text_company + str(tag_company[0].get('content'))

                    # 기사 작성 날짜
                    tag_date = document_content.find_all('span', {'class': 't11'})
                    text_date = ''
                    text_date = text_date + str(tag_date[0].find_all(text=True)[0])
                    if not text_date:
                        continue

                    self.done_aid.append(aid)
                    batch[aid] = {"category": category, "aid": aid, "date": text_date, "title": text_headline, \
                                  "content": text_sentence, "company": text_company}

                    del text_company, text_sentence, text_headline
                    del tag_company
                    del tag_content, tag_headline
                    del request_content, document_content

                except IndexError:
                    value = {"aid": aid, "url": url}
                    failed_urls.append(value)
                    print(f"failed: {value}")
                    del request_content, document_content
                    pass
                except Exception as e:  # UnicodeEncodeError ..
                    print(f"Parsing failed for url:{url}, Error: {e}")
                    value = {"aid": aid, "url": url}
                    failed_urls.append(value)
                    print(f"failed: {value}")
                    del request_content, document_content
                    pass

            # 파일 이름이 중복될 수도 있으니 구분자로 랜덤 숫자을 파일이름에 붙여준다
            file_name = f"{str(self.start_date)}_{str(self.end_date)}_{i}_{delimiter}"
            try:
                Writer.write_json_to_s3(category_name, batch, file_name)
                print(f"writing {category_name}/{file_name}.json is Done.")
            except Exception as e:
                print(f"Failed to write in s3: {category_name}, {self.start_date}, {self.end_date}, batch: {i}")

        if failed_urls:
            # 실패한 애들은 따로 DB 에 넣어준다
            Writer.insert_values_to_db('failed_urls', failed_urls)
            failed_count = len(failed_urls)
            del failed_urls

        # 크롤링된 id는 db에서 news_crawled = true로 바꿔준다
        batch_size = 2000
        i = 0
        for i in range(int(len(self.done_aid) / batch_size) + 1):
            batch = self.done_aid[i * batch_size: (i + 1) * batch_size]

            Writer.update_metadata_crawled_true(batch)

        print(f"Every Work on {category_name} {self.start_date} ~ {self.end_date} Done.\
              success: {len(self.done_aid)} passed: {len(crawling_targets) - len(self.done_aid) - failed_count}\
              Failed: {failed_count}")

        return "Done"

    def get_url_data(self, url: str, max_tries=10):
        remaining_tries = int(max_tries)

        while remaining_tries > 0:
            try:
                return requests.get(url, headers=self.headers)
            except requests.exceptions:
                sleep(60)
            remaining_tries = remaining_tries - 1
        raise ResponseTimeout()

    def start(self):
        # MultiProcess 크롤링 시작
        procs = []
        for category_name in self.selected_categories:
            proc = Process(target=self.crawling, args=(category_name,))
            procs.append(proc)
            proc.start()
        for proc in procs:
            proc.join()


if __name__ == "__main__":
    Crawler = ArticleCrawler('20200901', '20200901')
    Crawler.set_category("IT과학", "정치")
    Crawler.start()
