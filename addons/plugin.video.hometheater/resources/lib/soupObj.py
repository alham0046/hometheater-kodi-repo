import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

def soupObject(url, strainer = ""):
    req = requests.get(url, headers=headers)
    if strainer:
        if isinstance(strainer, re.Pattern):
            strainer = SoupStrainer('div', attrs={'class':strainer})
        elif strainer.startswith('.'):
            strainer = SoupStrainer('div', attrs={'class':strainer.split('.')[1]})
            # return BeautifulSoup(req.content, 'html.parser', parse_only=strainer)
        elif strainer.startswith('#'):
            strainer = SoupStrainer('div', attrs={'id':strainer.split('#')[1]})
        return BeautifulSoup(req.content, 'html.parser', parse_only=strainer)
    else :
        return BeautifulSoup(req.content, 'html.parser')