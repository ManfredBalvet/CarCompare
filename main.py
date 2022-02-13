from crawler import crawl
from datetime import datetime
from scraper import scrape
from get_headers import get_headers


if __name__ == "__main__":
    startTime = datetime.now()
    url = "https://www.guideautoweb.com/constructeurs/"
    print("Getting the URL for every car in " + url)
    urls = crawl(url)
    print("Getting information for all " + str(len(urls)) + " cars in the list")
    all_car_data = scrape(urls)
    print(all_car_data)
    headers = get_headers(all_car_data)
    print(headers)
    print("Done in " + str(datetime.now() - startTime) + " for all " + str(len(urls)) + " cars")
