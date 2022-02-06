from crawler import crawl
from datetime import datetime

startTime = datetime.now()

if __name__ == "__main__":
    print(crawl())

print(datetime.now() - startTime)
