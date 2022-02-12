from url_opener import download_url
from html.parser import HTMLParser


def crawl(url: str) -> list[str]:
    manufacturers_url = __crawl_manufacturers(url)
    versions_url = []
    for manufacturer_url in manufacturers_url:
        models_url = __crawl_models(manufacturer_url)
        for model_url in models_url:
            years_url = __crawl_years(model_url)
            for year_url in years_url:
                versions_url.extend(__crawl_versions(year_url))
                for version_url in versions_url:
                    print("Adding to the list " + version_url)

    return versions_url


def __crawl_manufacturers(url: str) -> list[str]:
    url_content = download_url(url)
    parser = ReadManufacturerHTML()
    parser.feed(url_content)

    return [url + manufacturer for manufacturer in parser.manufacturers]


def __crawl_models(manufacturer_url: str) -> list[str]:
    url_content = download_url(manufacturer_url)
    parser = ReadModelHTML()
    parser.feed(url_content)

    return [manufacturer_url + model for model in parser.models]


def __crawl_years(model_url: str) -> list[str]:
    url_content = download_url(model_url)
    parser = ReadYearHTML()
    parser.feed(url_content)

    return [model_url + "/" + year for year in parser.years]


def __get_specs_url(year_url: str) -> str:
    url_content = download_url(year_url)
    parser = ReadSpecHTML()
    parser.feed(url_content)

    return year_url + "/specifications/" + parser.spec


def __crawl_versions(year_url: str) -> list[str]:
    specs_url = __get_specs_url(year_url)
    url_content = download_url(specs_url)
    parser = ReadVersionHTML()
    parser.feed(url_content)

    return [specs_url.rsplit("/", 2)[0] + "/specifications/" + version for version in parser.versions]


class ReadManufacturerHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.manufacturers = []
        self.this_attrs = ""
        self.last_attrs = ""

    def handle_starttag(self, tag, attrs):
        self.last_attrs = self.this_attrs
        self.this_attrs = attrs

    def handle_data(self, data):
        if len(self.last_attrs) > 0 and "\n" not in data:
            if "href" in self.last_attrs[0][0] and "/constructeurs/" in self.last_attrs[0][1] and len(self.last_attrs[0][1].split("/")[2]) > 0:
                self.manufacturers.append(self.last_attrs[0][1].split("/")[2] + "/")


class ReadModelHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.this_tag = ""
        self.this_attrs = ""
        self.models = []

    def handle_starttag(self, tag, attrs):
        self.this_tag = tag
        self.this_attrs = attrs

    def handle_data(self, data):
        if len(self.this_attrs) == 2 and "\n" not in data:
            if self.this_tag == "a" and "constructeurs" in self.this_attrs[0][1]:
                self.models.append(self.this_attrs[0][1].split("/")[3])


class ReadYearHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.this_tag = ""
        self.this_attrs = ""
        self.years = []

    def handle_starttag(self, tag, attrs):
        self.this_tag = tag
        self.this_attrs = attrs

    def handle_data(self, data):
        if len(self.this_attrs) > 0 and "\n" not in data:
            if self.this_tag == "option" and "constructeurs" in self.this_attrs[0][1]:
                self.years.append(self.this_attrs[0][1].split("/")[4])


class ReadSpecHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.this_tag = ""
        self.this_attrs = ""
        self.spec = ""

    def handle_starttag(self, tag, attrs):
        self.this_tag = tag
        self.this_attrs = attrs

    def handle_data(self, data):
        if len(self.this_attrs) > 0 and "\n" not in data:
            if data == "Spécifications":
                self.spec = self.this_attrs[0][1].split("/")[6]


class ReadVersionHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.this_tag = ""
        self.this_attrs = ""
        self.versions = []

    def handle_starttag(self, tag, attrs):
        self.this_tag = tag
        self.this_attrs = attrs

    def handle_data(self, data):
        if len(self.this_attrs) > 0 and "\n" not in data:
            if self.this_tag == "option" and ("constructeurs" in self.this_attrs[0][1]) and (len(self.this_attrs[0][1].split("/")) > 6):
                self.versions.append(self.this_attrs[0][1].split("/")[6])
