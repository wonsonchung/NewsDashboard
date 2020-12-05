from NewsCrawler import news_crawler
import time

categories = {'정치': 100, '경제': 101, '사회': 102, '생활문화': 103, '세계': 104, 'IT과학': 105, '오피니언': 110}

# 시작날짜, 종료날짜를 '2020xxxx' 형식에 맞게 넣어주세욥!

start_date = 20200901
end_date = 20200902 # date는 이상/이하 조건으로 들어가므로 end_date 도 긁어옵니다.
batch = 1 # 3일 단위로 묶어서 크롤
for i in range((end_date - start_date -1)//batch + 1):
    start = start_date + i * batch
    end = start_date + (i + 1) * batch - 1
    if end > end_date:
        end = end_date
    Crawler = news_crawler.ArticleCrawler(str(start), str(end))
    # 오타 없나 체크 또 체크!
    Crawler.set_category('정치', '경제','사회', '생활문화', '세계', 'IT과학', '오피니언')
    print(f"Crawling {start} ~ {end} start!")
    Crawler.start()
    print(f"Crawling {start} ~ {end} Done!")

    time.sleep(60)
