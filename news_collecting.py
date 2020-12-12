from NewsCrawler import news_crawler
from NewsCrawler.category import categories, reversed_categories
import time
import argparse


# 시작날짜, 종료날짜를 '2020xxxx' 형식에 맞게 넣어주세욥!
parser = argparse.ArgumentParser(description='Date Configuration')
parser.add_argument('--start', required=True, help='start date of crawling ex.20200901')
parser.add_argument('--end', required=True, help='end date of crawling ex.20200910')
parser.add_argument('--category', required=False, help='put category in string or int')

args = parser.parse_args()

start_date, end_date = int(args.start), int(args.end)
category = args.category.strip().split(',')

for i, cate in enumerate(category):
    if cate in categories:
        continue
    elif int(cate) in reversed_categories:
        category[i] = reversed_categories[int(cate)]
    else:
        raise KeyError

# start crawler
batch = 3 # 3일 단위로 묶어서 크롤링
for i in range((end_date - start_date)//batch + 1):
    start_time = time.time()

    start = start_date + i * batch
    end = start_date + (i + 1) * batch - 1
    if end > end_date:
        end = end_date
    Crawler = news_crawler.ArticleCrawler(str(start), str(end))
    # 오타 없나 체크 또 체크!
    Crawler.set_category(category)
    print(f"Crawling {start} ~ {end} start!")
    Crawler.start()
    print(f"Crawling {start} ~ {end} Done!")
    print(f"==========================={time.time() - start_time} seconds ============================")

    time.sleep(30)
