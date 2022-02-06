from urllib import request
import re


def crawl() -> list[str]:
    manufacturers_url = __crawl_manufacturers()
    versions_url = []
    for manufacturer_url in manufacturers_url:
        models_url = __crawl_models(manufacturer_url)
        for model_url in models_url:
            years_url = __crawl_years(model_url)
            for year_url in years_url:
                print(year_url)
                versions_url.extend(__crawl_versions(year_url))

    return versions_url


def __download_url(url: str) -> str:
    web_content = ""
    try:
        response = request.urlopen(url)
        web_content = response.read().decode('UTF-8')
    except:
        pass

    return web_content


def __crawl_manufacturers() -> list[str]:
    url = "https://www.guideautoweb.com/constructeurs/"
    url_content = __download_url(url)
    if __download_url(url) == "":
        manufacturers = ""
    else:
        pattern_start = "href=\"/constructeurs/"
        pattern_end = "\""
        pattern = pattern_start + "([^'\"]+)" + pattern_end
        manufacturers = re.findall(pattern, url_content)

    return [url + manufacturer for manufacturer in manufacturers]


def __crawl_models(manufacturer_url: str) -> list[str]:
    url_content = __download_url(manufacturer_url)
    if __download_url(manufacturer_url) == "":
        models = ""
    else:
        url_start = manufacturer_url.split("https://www.guideautoweb.com")[1]
        pattern_start = "href=\"" + url_start
        pattern_end = "\""
        pattern = pattern_start + "([^'\"]+)" + pattern_end
        models = re.findall(pattern, url_content)

    return [manufacturer_url + model for model in set(models)]


def __crawl_years(model_url: str) -> list[str]:
    url_content = __download_url(model_url)
    if __download_url(model_url) == "":
        years = ""
    else:
        url_start = model_url.split("https://www.guideautoweb.com")[1].rsplit("/", 2)[0]
        pattern_start = "<option value=\"" + url_start
        pattern_end = "\">"
        pattern = pattern_start + "([^'\"]+)" + pattern_end
        years = re.findall(pattern, url_content)

    return [model_url.rsplit("/", 2)[0] + year for year in set(years)]


def __crawl_versions(year_url: str) -> list[str]:
    specs_url = __get_specs_url(year_url)
    url_content = __download_url(specs_url)
    if __download_url(specs_url) == "":
        versions = ""
    else:
        url_start = specs_url.split("https://www.guideautoweb.com")[1].rsplit("/", 2)[0]
        pattern_start = "<option value=\"" + url_start + "/"
        pattern_end = "\""
        pattern = pattern_start + "([^'\"]+/)" + pattern_end
        versions = re.findall(pattern, url_content)

    return [specs_url.rsplit("/", 2)[0] + "/" + version for version in set(versions)]


def __get_specs_url(year_url: str) -> str:
    url_content = __download_url(year_url)
    if __download_url(year_url) == "":
        specs_url = ""
    else:
        url_start = year_url.split("https://www.guideautoweb.com")[1]
        pattern_start = "href=\"" + url_start + "specifications/"
        pattern_end = "\""
        pattern = pattern_start + "([^'\"]+/)" + pattern_end
        specs = re.findall(pattern, url_content)
        specs_url = year_url + "specifications/" + specs[0]

    return specs_url
