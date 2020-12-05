from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
from typing import List, Dict
from NewsCrawler.exceptions import *


class ArticleParser(object):
    special_symbol = re.compile('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$&▲▶◆◀■【】\\\=\(\'\"]')
    content_pattern = re.compile('본문 내용|TV플레이어| 동영상 뉴스|flash 오류를 우회하기 위한 함수 추가function  flash removeCallback|tt|앵커 멘트|xa0')

    @classmethod
    def clear_content(cls, text: str) -> str:
        # 기사 본문에서 필요없는 특수문자 및 본문 양식 등을 다 지움
        newline_symbol_removed_text = text.replace('\\n', '').replace('\\t', '').replace('\\r', '')
        special_symbol_removed_content = re.sub(cls.special_symbol, ' ', newline_symbol_removed_text)
        end_phrase_removed_content = re.sub(cls.content_pattern, '', special_symbol_removed_content)
        blank_removed_content = re.sub(' +', ' ', end_phrase_removed_content).lstrip()  # 공백 에러 삭제
        reversed_content = ''.join(reversed(blank_removed_content))  # 기사 내용을 reverse 한다.
        content = ''
        for i in range(0, len(blank_removed_content)):
            # reverse 된 기사 내용중, ".다"로 끝나는 경우 기사 내용이 끝난 것이기 때문에 기사 내용이 끝난 후의 광고, 기자 등의 정보는 다 지움
            if reversed_content[i:i + 2] == '.다':
                content = ''.join(reversed(reversed_content[i:]))
                break
        return content

    @classmethod
    def clear_headline(cls, text: str) -> str:
        # 기사 제목에서 필요없는 특수문자들을 지움
        newline_symbol_removed_text = text.replace('\\n', '').replace('\\t', '').replace('\\r', '')
        special_symbol_removed_headline = re.sub(cls.special_symbol, '', newline_symbol_removed_text)
        return special_symbol_removed_headline

    @classmethod
    def create_metadata(cls, URL: str, text: str) -> Dict:
        """DB에 넣기 위해 url을 파싱하고 날짜 데이터와 현재 시간을 이용해 뉴스의 메타데이터를 만든다."""
        crawled_time = str(datetime.now())
        # metadata 초기화(스키마를 만드는 역할도 함)
        metadata = {'upload_date': '20200000', 'category': '0', 'oid': '0', 'aid': str(0),
                    'url': text, 'news_crawled': 'false', 'initial_update': crawled_time}

        try:
            date = URL.split('&')[-2].split('=')[1]
            sid1 = text.split('&')[-3].split('=')[1]
            oid = text.split('&')[-2].split('=')[1]
            aid = text.split('&')[-1].split('=')[1]
        except Exception:
            raise UrlStructureError(URL, text)

        metadata['upload_date'] = str(date)
        metadata['category'] = str(sid1)
        metadata['oid'] = str(oid)
        metadata['aid'] = str(aid)
        metadata['url'] = text
        metadata['initial_update'] = crawled_time

        return metadata




