from url_opener import download_url


def scrape(urls: list[str]) -> list[list[str]]:
    all_car_data = []
    parser = ReadHTML()
    for url in urls:
        url_content = download_url(url)
        url_parts = url.rsplit("/")
        car_data = [
            ["Manufacturier", url_parts[4]],
            ["Modèle", url_parts[5]],
            ["Année", url_parts[6]],
        ]
        parser.feed(url_content)
        car_data.extend(parser.this_car_data)
        print("Adding information for " + car_data[0][1] + " " + car_data[1][1] + " " + car_data[2][1] + " " + car_data[3][1])
        parser.last_tag = ""
        parser.this_tag = ""
        parser.this_car_data = []
        parser.possible_header = ""
        parser.this_attrs = ""
        parser.motor = 0
        parser.end_tag = ""
        parser.new_motor = False

        all_car_data.append(car_data)

    return all_car_data


class ReadHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.last_tag = ""
        self.this_tag = ""
        self.this_car_data = []
        self.possible_header = ""
        self.this_attrs = ""
        self.motor = 0
        self.end_tag = ""
        self.new_motor = False
        self.motor_spec = ["Moteur", "Puissance", "Couple", "Alimentation", "Type de carburant"]  # TODO: Not do it hard coded??

    def handle_starttag(self, tag, attrs):
        self.last_tag = self.this_tag
        self.this_tag = tag
        self.this_attrs = attrs

    def handle_data(self, data):
        if "\n" in data:
            pass
        else:
            if self.this_tag == "th" or (self.this_tag == "abbr" and self.last_tag == "th"):
                self.possible_header = data.replace("\xa0", " ")

            if self.this_tag == "td" or (self.this_tag == "abbr" and self.last_tag == "td"):
                if self.possible_header == "Moteur":
                    self.motor += 1
                if self.possible_header in self.motor_spec:
                    self.possible_header = self.possible_header + " " + str(self.motor)

                self.this_car_data.extend([[self.possible_header, data.replace("\xa0", " ")]])

            if self.this_tag == "option" and len(self.this_attrs) == 2:
                if "selected" in self.this_attrs[1]:
                    self.this_car_data = [["Version", data.split(" - ")[0]]]
