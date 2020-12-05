from NewsCrawler import url_crawler

categories = {'정치': 100, '경제': 101, '사회': 102, '생활문화': 103, '세계': 104, 'IT과학': 105, '오피니언': 110}
keys = list(categories.keys())
Crawler = url_crawler.UrlCrawler()

Crawler.set_category('정치', '경제', '사회', '생활문화', '세계', 'IT과학', '오피니언')
Crawler.set_date_range(11, 16, 11, 20)
Crawler.start()