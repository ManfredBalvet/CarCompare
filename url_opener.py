from urllib import request


def download_url(url: str) -> str:
    web_content = ""
    try:
        response = request.urlopen(url)
        web_content = response.read().decode('UTF-8')
    except:
        pass

    return web_content
