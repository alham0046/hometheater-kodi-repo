import requests
from bs4 import BeautifulSoup

mainUrl = "https://www.yodesitv.info/"
channelList = ["star plus", "sony tv", "star bharat", "zee tv", "colors", "sab tv"]

def fetchShows(channels):
    for channel in channels:
        churl = mainUrl + "-".join(channel.split(" "))
        print(churl)

fetchShows(channelList)