from crawler import crawl
from datetime import datetime
from scraper import scrape
from url_opener import download_url
import re

# startTime = datetime.now()
# if __name__ == "__main__":
#     urls = crawl()
#     all_car_data = scrape(urls)
#     test = scrape(["https://www.guideautoweb.com/constructeurs/toyota/86/2020/specifications/gt-man/"])
#     print(dir(test))
#
# print(datetime.now() - startTime)

url_content = download_url("https://www.guideautoweb.com/constructeurs/toyota/86/2020/specifications/gt-man/")
print(url_content)
pattern_start = "<tr>"
pattern_end = "</tr>"
pattern = pattern_start + "(.+)" + pattern_end

trs = re.findall(pattern, url_content)
print(trs)
