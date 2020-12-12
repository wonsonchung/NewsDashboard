from NewsCrawler import url_crawler
from NewsCrawler.category import categories, reversed_categories
import argparse

parser = argparse.ArgumentParser(description='Date Configuration')
parser.add_argument('--start', required=True, help='start date of crawling ex.0901')
parser.add_argument('--end', required=True, help='end date of crawling ex.0910')
parser.add_argument('--category', required=False, help='')

args = parser.parse_args()

start_month, start_day = int(args.start[:2]), int(args.start[2:])
end_month, end_day = int(args.end[:2]), int(args.end[2:])

category = args.category.strip().split(',')

for i, cate in enumerate(category):
    if cate in categories:
        continue
    elif int(cate) in reversed_categories:
        category[i] = reversed_categories[int(cate)]
    else:
        raise KeyError

Crawler = url_crawler.UrlCrawler()
Crawler.set_category(category)
Crawler.set_date_range(start_month, start_day, end_month, end_day)
Crawler.start()