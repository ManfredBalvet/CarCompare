from crawler import crawl
from datetime import datetime
from scraper import scrape
from url_opener import download_url
import re

startTime = datetime.now()

if __name__ == "__main__":
    url = "https://www.guideautoweb.com/constructeurs/"
    print("Getting the URL for every car in " + url)
    urls = crawl(url)
    print("Getting information for all " + str(len(urls)) + " cars in the list")
    all_car_data = scrape(urls)
    print(all_car_data)

print("Done in: " + str(datetime.now() - startTime))
