

def get_headers(all_car_data: list[list[str]]) -> list[str]:
    all_headers = set()
    headers = []
    for car_data in all_car_data:
        previous_index = -1
        for i, [header, data] in enumerate(car_data):
            if header not in all_headers:
                all_headers.add(header)
                headers.insert(previous_index + 1, header)
            previous_index = i

    return headers
