from collections import namedtuple
import requests
from bs4 import BeautifulSoup as bs


def parse(url):
    #if url.endswith('.pdf'):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
    try:
        page = requests.get(url, headers=headers)
        if page.status_code == 200:
            return True
        else:
            return True
    except Exception:
        return True


