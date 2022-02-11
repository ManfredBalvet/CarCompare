from car_data import CarData
import re
from url_opener import download_url


def scrape(urls: list[str]) -> list[CarData]:
    all_car_data = []
    for url in urls:
        manufacturer = url.rsplit("/")[4]
        model = url.rsplit("/")[5]
        year = url.rsplit("/")[6]
        version = url.rsplit("/")[8]
        car_from_url = CarData(manufacturer, model, year, version)
        trs = __get_tr(url)
        print("trs: ", trs)
        for tr in trs:
            print(tr)
            th = __get_th(tr)
            td = __get_td(tr)
            print(3, th, td)
            setattr(car_from_url, th, td)
        all_car_data.append(car_from_url)

    return all_car_data


def __get_tr(url: str) -> list[str]:
    url_content = download_url(url)
    if url_content == "":
        trs = ""
    else:
        pattern_start = "<tr>"
        pattern_end = "</tr>"
        pattern = pattern_start + "(.+)" + pattern_end
        print("Pattern: ", pattern)
        trs = re.findall(pattern, url_content)  # TODO

    return trs


def __get_th(tr: str) -> str:
    pattern_start = "<th>"
    pattern_end = "</th>"
    pattern = pattern_start + "(.+)" + pattern_end
    th = re.findall(pattern, tr)[0]
    print("th: ", th)

    return __if_abbr(th)


def __get_td(tr: str) -> str:
    pattern_start = "<td>"
    pattern_end = "</td>"
    pattern = pattern_start + "(.+)" + pattern_end
    td = re.findall(pattern, tr)[0]
    print("td: ", td)

    return __if_abbr(td)


def __if_abbr(t: str) -> str:
    if "abbr" in t:
        t = re.findall(">" + "(.+)" + "<", t)[0]

    return t
