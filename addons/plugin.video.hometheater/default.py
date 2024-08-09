import sys
import xbmc
import urllib.parse
import xbmcplugin
import xbmcgui
import xbmcvfs
import xbmcaddon
import sqlite3
import re
from resources.lib import tmdbfetch
from resources.lib import urlResolver
import concurrent.futures
import shelve
import os
from resources.lib.router import routing

# from resolveurl import HostedMediaFile
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import requests

# Plugin base URL
base_url = sys.argv[0]

# Addon instance
addon = xbmcaddon.Addon()



# URL and headers for web scraping
urlmain = "https://www.yodesitv.info/"
moviesUrl = "https://luxmovies.live"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}
channelList = ["Star Plus", "Sony TV", "Star Bharat", "Zee TV"]
popularOtts = ['netflix', 'disney', 'hotstar', 'amazon', 'prime', 'sony', 'sonyliv', 'zee', 'zee5', 'jio', 'jiocinema', 'mxplayer']

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

def get_shows(showurl):
    xbmc.log(f"Fetching shows from URL: {showurl}", xbmc.LOGDEBUG)
    shows = soupObject(showurl, re.compile('^one_'))
    showLists = shows.find_all('p', attrs={'class': 'small-title'})
    for showList in showLists:
        li = xbmcgui.ListItem(showList.text)
        showurl = build_url({'mode': 'get_Episodes', 'url': showList.find('a').get('href')})
        xbmc.log(f"Adding show to directory: {showList.text} with URL: {showurl}", xbmc.LOGDEBUG)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=showurl, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

def get_Episodes(episodeUrl):
    xbmc.log(f"Fetching episodes from URL: {episodeUrl}", xbmc.LOGDEBUG)
    episodeSoup = soupObject(episodeUrl, '#content_box')
    episodes = episodeSoup.select('h2.front-view-title')
    for episode in episodes:
        li = xbmcgui.ListItem(episode.text)
        li.setProperty('IsPlayable', 'true')
        vidurl = build_url({'mode': 'play_video', 'url': episode.find('a').get('href')})
        xbmc.log(f"Adding episode to directory: {episode.text} with URL: {vidurl}", xbmc.LOGDEBUG)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=vidurl, listitem=li, isFolder=False)
    xbmcplugin.endOfDirectory(addon_handle)

def get_tag(tag):
    return tag.name == 'span' and 'TVlogy' in tag.text
    # return tag.name == 'span' and 'VKprime' in tag.text

def shorten(url):
    base_Url = 'http://tinyurl.com/api-create.php?url='
    resp = requests.get(base_Url+url)
    shortUrl = resp.text
    return shortUrl

# def check_hosted_media(vid_url, subs=False):
#     from resolveurl import HostedMediaFile
#     return HostedMediaFile(url=vid_url, subs=subs)

# def resolve_url(url, subs=False):
#     hmf = check_hosted_media(url, subs)

#     try:
#         if subs:
#             resp = hmf.resolve()
#             stream_url = resp.get('url')
#         else:
#             stream_url = hmf.resolve()
#     except Exception as e:
#         try:
#             msg = str(e)
#         except:
#             msg = url
#         xbmcgui.Dialog().notification(msg, 'Resolve URL', 5000)
#         return False

#     if subs:
#         return resp
#     return stream_url

def get_VideoLink(vidurl):
    videoLinkSoup = soupObject(vidurl, '.thecontent')
    links = videoLinkSoup.find(get_tag).parent.find_next_sibling('p').select_one('a')['href']
    linkSoup = soupObject(links, '#content')
    iframe = linkSoup.select_one('iframe').get('src')
    stream_Url = urlResolver.resolve_url(iframe, subs=True)
    # vidres = soupObject(iframe)
    # img = vidres.find_all('img')
    # scripts = vidres.find_all('script')
    # midlinkarr = scripts[-2].text.split('|')
    # midlink = midlinkarr[midlinkarr.index("sources") -1]
    # firstLink = img[0].get('src').split('i/')[0]
    # lastLink = '/v.mp4'
    # link = firstLink + midlink + lastLink
    # return link
    return stream_Url

def play_video(video_url):
    test_link = get_VideoLink(video_url)
    stream_Link = test_link.get('url')
    li = xbmcgui.ListItem(offscreen = True)
    # li.setProperty('IsPlayable', 'true')
    li.setPath(stream_Link)
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=li)

def get_movieplatform():
    ottAppsSoup = soupObject(moviesUrl)
    ottApps = ottAppsSoup.select('div#header-category a span')
    pattern = re.compile(r'^[A-Za-z]')
    for ottApp in ottApps:
        if pattern.match(ottApp.text.strip()) and any(ott in ottApp.text.strip().lower() for ott in popularOtts):
            li = xbmcgui.ListItem(ottApp.text.strip())
            url = build_url({'mode': 'get_movies', 'url': moviesUrl + ottApp.parent['href']})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
            # print(ottApp.text.strip())
    
    xbmcplugin.endOfDirectory(addon_handle)


def get_channel():
    xbmc.log(f"Fetching channels from URL: {urlmain}", xbmc.LOGDEBUG)
    soup = soupObject(urlmain, '.secondary-navigation')
    channels = soup.find_all('li', attrs={'class': 'menu-item-type-post_type'})
    for channel in channels:
        if channel.text.strip() in channelList:
            li = xbmcgui.ListItem(channel.text.strip())
            url = build_url({'mode': 'get_shows', 'url': channel.find('a').get('href')})
            xbmc.log(f"Adding channel to directory: {channel.text.strip()} with URL: {url}", xbmc.LOGDEBUG)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

def get_MoviesLink(url):
    MovieQualitySoup = soupObject(url)
    # start = time.time()
    scriptPattern= r"var url = '([^']+)'"
    # pattern = r'{\d{4}}.+\b1080p\b.+'
    qualityUrl = MovieQualitySoup.select_one('div.entry-content h5:has(span:-soup-contains("1080p"))').find_next_sibling('p').select_one('a')['href']
    # qualityUrl = MovieQualitySoup.find('span', text=lambda text: text and pattern in text).find_next_sibling('p').select_one('a')['href']
    vcloudSoup = soupObject(qualityUrl)
    VcloudUrl = vcloudSoup.select_one('div.entry-content p a:has(button:-soup-contains("V-Cloud"))')['href']
    playableSoup = soupObject(VcloudUrl)
    linkJsScript = playableSoup.select('div.card script')[1].text
    playableUrl = re.search(scriptPattern, linkJsScript).group(1)
    mp4Soup = soupObject(playableUrl)
    mp4arr = mp4Soup.select('a[href$=".mkv"], a[href$=".mp4"], a[href$=".avi"] ')
    if len(mp4arr) > 0:
        mp4Url = mp4arr[0]['href']
        return mp4Url
    elif "gofile" in mp4Soup.get_text().lower() :
        gofileUrl = mp4Soup.select_one('a[href*="gofile"]')['href']
        gofileReq = requests.get(gofileUrl)
        gofileSoup = BeautifulSoup(gofileReq.text, 'html.parser')
        mp4Url = gofileSoup.select_one('meta[content*="https"]')['content'].replace("store2", "file5").replace("thumb_", "").replace(".jpg", "")
        return mp4Url

def play_movie(video_url):
    # test_link = get_cached_link(video_url)
    # if not test_link:
    test_link = get_MoviesLink(video_url)
        # save_to_cache(video_url, test_link)
    li = xbmcgui.ListItem(offscreen = True)
    li.setPath(test_link)
    # player = xbmc.Player()
    # player.play(test_link, listitem=li)
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=li)

# def get_moviesList(url):
#     mainCategory = soupObject(url, '.listing-content')
#     linkTagspre = mainCategory.select('a')
#     linkTags = [a for a in linkTagspre if 'season' not in a.get('title').lower()]
#     pattern = r"download-(.*?)(19[0-9]{2}|20[0-3][0-9])"
#     for i in range(2, 4):
#         link = url + f"/page/{i}"
#         if requests.get(link):
#             pages = soupObject(link, '.listing-content')
#             pagesTagspre = pages.select('a')
#             pagesTags = [a for a in pagesTagspre if 'season' not in a.get('title').lower()]
#             linkTags.extend(pagesTags)
#         else:
#             break

#     for linkTag in linkTags:
#         findTitle = re.search(pattern, linkTag['href'])
#         if findTitle:
#             MovieName = findTitle.group(1).replace('-', ' ').strip()
#             li = xbmcgui.ListItem(MovieName)
#             li.setProperty('IsPlayable', 'true')
#             # # Fetch movie details from TMDB using TMDB Helper
#             # xbmc.log(f"Fetching TMDB details for movie: {MovieName}", xbmc.LOGDEBUG)
#             tmdb_details = tmdbfetch.fetch_tmdb_details(MovieName)
#             if tmdb_details:
#                 li.setArt({
#                     'thumb': tmdb_details['poster_path'],  # Set the thumbnail image
#                     'icon': tmdb_details['poster_path'],   # Set the icon image (optional)
#                     'fanart': tmdb_details['backdrop_path']  # Set the fanart image (optional)
#                 })
#             #     image_url = tmdb_details['poster_path']
#             #     xbmc.log(f"Found image URL: {image_url}", xbmc.LOGDEBUG)
#             else:
#             #     xbmc.log(f"No image found for: {MovieName}", xbmc.LOGDEBUG)
#             #     # image_url = ''
#                 image_url = 'https://luxmovies.live/wp-content/uploads/2024/05/Crew-165x248.jpg'

#             url = build_url({'mode': 'play_movie', 'url': linkTag['href']})
#             xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
#     xbmcplugin.endOfDirectory(addon_handle)


# def fetch_and_set_tmdb_details(li, MovieName, href):
#     # Fetch movie details from TMDB using TMDB Helper
#     tmdb_details = tmdbfetch.fetch_tmdb_details(MovieName)
#     if tmdb_details:
#         li.setArt({
#             'thumb': tmdb_details['poster_path'],  # Set the thumbnail image
#             'icon': tmdb_details['poster_path'],   # Set the icon image (optional)
#             'fanart': tmdb_details['backdrop_path']  # Set the fanart image (optional)
#         })
#     else:
#         image_url = 'https://luxmovies.live/wp-content/uploads/2024/05/Crew-165x248.jpg'
    
#     url = build_url({'mode': 'play_movie', 'url': href})
#     return li, url


# def fetch_page_links(page_number, BASE_URL):
#     link = f"{BASE_URL}/page/{page_number}"
#     response = requests.get(link)
#     if response.status_code == 200:
#         pages = soupObject(link, '.listing-content')
#         return [a for a in pages.select('a') if 'season' not in a.get('title').lower()]
#     return []


# def get_moviesList(url):
#     mainCategory = soupObject(url, '.listing-content')
#     linkTags = [a for a in mainCategory.select('a') if 'season' not in a.get('title').lower()]
#     pattern = r"download-(.*?)(19[0-9]{2}|20[0-3][0-9])"

#     # Fetch additional pages concurrently
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         futures = [executor.submit(fetch_page_links, i, url) for i in range(2, 4)]
#         for future in concurrent.futures.as_completed(futures):
#             linkTags.extend(future.result())

#     # Process the links and fetch TMDB details concurrently
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         futures = []
#         for linkTag in linkTags:
#             findTitle = re.search(pattern, linkTag['href'])
#             if findTitle:
#                 MovieName = findTitle.group(1).replace('-', ' ').strip()
#                 li = xbmcgui.ListItem(MovieName)
#                 li.setProperty('IsPlayable', 'true')
#                 futures.append(executor.submit(fetch_and_set_tmdb_details, li, MovieName, linkTag['href']))

#         # Add directory items once details are fetched
#         for future in concurrent.futures.as_completed(futures):
#             li, url = future.result()
#             xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)

#     xbmcplugin.endOfDirectory(addon_handle)


def fetch_page_links(page_number, BASE_URL):
    link = f"{BASE_URL}/page/{page_number}"
    response = requests.get(link)
    if response.status_code == 200:
        pages = soupObject(link, '.listing-content')
        return [a for a in pages.select('a') if 'season' not in a.get('title').lower()]
    return []

def get_moviesList(url):
    mainCategory = soupObject(url, '.listing-content')
    linkTags = [a for a in mainCategory.select('a') if 'season' not in a.get('title').lower()]
    pattern = r"download-(.*?)(19[0-9]{2}|20[0-3][0-9])"

    # Fetch additional pages concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_page_links, i, url) for i in range(2, 4)]
        for future in concurrent.futures.as_completed(futures):
            linkTags.extend(future.result())

    # List to store movies with their respective URLs
    movies = []
    for linkTag in linkTags:
        findTitle = re.search(pattern, linkTag['href'])
        if findTitle:
            MovieName = findTitle.group(1).replace('-', ' ').strip()
            movies.append((MovieName, linkTag['href']))

    # Fetch TMDB details concurrently while preserving order
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_and_set_tmdb_details, MovieName, href) for MovieName, href in movies]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    # Add directory items in the correct order
    for result in results:
        li, url = result
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)

    xbmcplugin.endOfDirectory(addon_handle)

def fetch_and_set_tmdb_details(MovieName, href):
    li = xbmcgui.ListItem(MovieName)
    li.setProperty('IsPlayable', 'true')

    # Fetch movie details from TMDB using TMDB Helper
    tmdb_details = tmdbfetch.fetch_tmdb_details(MovieName)
    if tmdb_details:
        li.setArt({
            'thumb': tmdb_details['poster_path'],  # Set the thumbnail image
            'icon': tmdb_details['poster_path'],   # Set the icon image (optional)
            'fanart': tmdb_details['backdrop_path']  # Set the fanart image (optional)
        })
    else:
        image_url = 'https://luxmovies.live/wp-content/uploads/2024/05/Crew-165x248.jpg'

    url = build_url({'mode': 'play_movie', 'url': href})
    return li, url


def build_url(query):
    return base_url + '?' + urllib.parse.urlencode(query)

def router(paramstring):
    params = dict(urllib.parse.parse_qsl(paramstring))
    if params:
        xbmc.log(f"Router params: {params}", xbmc.LOGDEBUG)
        if params['mode'] == 'get_channel':
            get_channel()
        elif params['mode'] == "get_movieplatform":
            xbmc.log(f"Router params movieplatform main: {params}", xbmc.LOGDEBUG)
            xbmc.log(f"Router params movieplatform main string: {paramstring}", xbmc.LOGDEBUG)
            get_movieplatform()
        elif params['mode'] == 'get_shows':
            get_shows(params['url'])
        elif params['mode'] == 'get_Episodes':
            get_Episodes(params['url'])
        elif params['mode'] == 'play_video':
            play_video(params['url'])
        elif params['mode'] == 'get_movies':
            get_moviesList(params['url'])
        elif params['mode'] == 'play_movie':
            play_movie(params['url'])
    else:
        xbmc.log(f"Router params: {params}", xbmc.LOGDEBUG)
        main_menu()


def main_menu():
    url = build_url({'mode': 'get_channel'})
    li = xbmcgui.ListItem('Channels')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    url = build_url({'mode': 'get_movieplatform'})
    li = xbmcgui.ListItem('Movies')
    xbmc.log(f"addon handle is : {addon_handle}", xbmc.LOGDEBUG)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)


if __name__ == '__main__':
    addon_handle = int(sys.argv[1])
    xbmc.log(f"Received paramstring: {sys.argv[2]}", xbmc.LOGDEBUG)
    # router(sys.argv[2][1:])
    routing(sys.argv[2][1:])
    # router(sys.argv[2])





exit()

import sys
import xbmc
import urllib.parse
import xbmcplugin
import xbmcgui
import xbmcaddon
from bs4 import BeautifulSoup
import requests

# Plugin base URL
base_url = sys.argv[0]

# Addon instance
addon = xbmcaddon.Addon()

# URL and headers for web scraping
urlmain = "https://www.yodesitv.info/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
channelList = ["Star Plus", "Sony TV", "Star Bharat", "Zee TV"]

def soupObject(url):
    req = requests.get(url, headers=headers)
    return BeautifulSoup(req.content, 'html.parser')

def get_shows(showurl):
    shows = soupObject(showurl)
    showLists = shows.find_all('p', attrs={'class':'small-title'})
    for showList in showLists:
        li = xbmcgui.ListItem(showList.text)
        showurl = build_url({'mode': 'get_Episodes', 'url': showList.find('a').get('href')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=showurl, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

def get_Episodes(episodeUrl):
    episodeSoup = soupObject(episodeUrl)
    episodes = episodeSoup.select('h2.front-view-title')
    for episode in episodes:
        li = xbmcgui.ListItem(episode.text)
        # vidurl = get_VideoLink(episode.find('a').get('href'))
        vidurl = build_url({'mode': 'play_video', 'url': episode.find('a').get('href')})
        # li.setInfo('video', {'title': episode.text})
        # li.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=vidurl, listitem=li, isFolder=False)
    xbmcplugin.endOfDirectory(addon_handle)

def get_tag(tag):
    return (tag.name == 'span' and 'VKprime' in tag.text)

def get_VideoLink(vidurl):
    videoLinkSoup = soupObject(vidurl)
    links = videoLinkSoup.find(get_tag).parent.find_next_sibling('p').select_one('a')['href']
    linkSoup = soupObject(links)
    iframe = linkSoup.select_one('iframe').get('src')
    vidres = soupObject(iframe)
    img = vidres.find_all('img')
    scripts = vidres.find_all('script')
    midlink = scripts[-2].text.split('|')[-6]
    firstLink = img[0].get('src').split('i')[0]
    lastLink = '/v.mp4'
    link = firstLink + midlink + lastLink
    return link

def play_video(video_url):
    # vidLink = get_VideoLink(video_url)
    # # li = xbmcgui.ListItem(vidLink)
    # # vidurl = build_url({'mode': 'play_videopagal', 'url': vidLink})
    # # xbmcplugin.addDirectoryItem(handle=addon_handle, url=vidurl, listitem=li, isFolder=False)
    # # xbmcplugin.endOfDirectory(addon_handle)
    # li = xbmcgui.ListItem(path=vidLink)
    # li.setInfo('video', {'title': 'Playing Video'})
    # li.setProperty('IsPlayable', 'true')
    # xbmcplugin.setResolvedUrl(addon_handle, True, listitem=li)
    test_link = "https://archive.org/download/ical-capcut/1.%207178132193749863682.mp4"  # Replace with a known working MP4 link
    xbmc.log(f"Play video called with URL: {video_url}", xbmc.LOGDEBUG)
    xbmc.log(f"Resolved video link: {test_link}", xbmc.LOGDEBUG)  # Log the test video link
    li = xbmcgui.ListItem(path=test_link)
    li.setInfo('video', {'title': 'Playing Video'})
    li.setProperty('IsPlayable', 'true')
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=li)

def get_channel():
    soup = soupObject(urlmain)
    channels = soup.find_all('li', attrs={'class':'menu-item-type-post_type'})
    for channel in channels:
        if channel.text.strip() in channelList:
            li = xbmcgui.ListItem(channel.text.strip())
            url = build_url({'mode': 'get_shows', 'url': channel.find('a').get('href')})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

def build_url(query):
    return base_url + '?' + urllib.parse.urlencode(query)

def router(paramstring):
    params = dict(urllib.parse.parse_qsl(paramstring))
    if params:
        if params['mode'] == 'get_channel':
            get_channel()
        elif params['mode'] == 'get_shows':
            get_shows(params['url'])
        elif params['mode'] == 'get_Episodes':
            get_Episodes(params['url'])
        elif params['mode'] == 'play_video':
            play_video(params['url'])
    else:
        main_menu()

def main_menu():
    url = build_url({'mode': 'get_channel'})
    li = xbmcgui.ListItem('Channels')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

if __name__ == '__main__':
    addon_handle = int(sys.argv[1])
    router(sys.argv[2][1:])
