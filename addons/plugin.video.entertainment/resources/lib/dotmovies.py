import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from resources.lib.soupObj import soupObject
import concurrent.futures
import re
import xbmcplugin
import xbmcgui
import xbmc
import sys
from resources.lib import tmdbfetch
import urllib.parse
from resources.lib.impfunctions import build_url, addon_handle


moviesUrl = "https://dotmovies.autos"
popularOtts = ['netflix', 'disney', 'hotstar', 'amazon', 'prime', 'sony', 'sonyliv', 'zee', 'zee5', 'jio', 'jiocinema', 'mxplayer']


def fetch_page_links(page_number, BASE_URL):
    link = f"{BASE_URL}/page/{page_number}"
    response = requests.get(link)
    if response.status_code == 200:
        pages = soupObject(link, '.inside-article')
        return [a for a in pages.select('h2>a') if 'season' not in a.text.lower()]
    return []

def get_movieplatform():
    ottAppsSoup = soupObject(moviesUrl, '#hm-category')
    ottApps = ottAppsSoup.select('a span')
    pattern = re.compile(r'^[A-Za-z]')
    for ottApp in ottApps:
        if pattern.match(ottApp.text.strip()) and any(ott in ottApp.text.strip().lower() for ott in popularOtts):
            li = xbmcgui.ListItem(ottApp.text.strip())
            url = build_url({'mode': 'get_movies', 'url': moviesUrl + ottApp.parent['href']})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
            # print(ottApp.text.strip())
    
    xbmcplugin.endOfDirectory(addon_handle)

#### this also gives old movies but better as some of new movies appears
def get_moviesList(url):
    mainCategory = soupObject(url, '.inside-article')
    linkTags = [a for a in mainCategory.select('h2>a') if 'season' not in a.text.lower()]
    pattern = r"Download (.*?)(19[0-9]{2}|20[0-3][0-9])"

    # Fetch additional pages concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_page_links, i, url) for i in range(2, 4)]
        for future in concurrent.futures.as_completed(futures):
            linkTags.extend(future.result())

    # List to store movies with their respective URLs
    movies = []
    for linkTag in linkTags:
        findTitle = re.search(pattern, linkTag.text)
        if findTitle:
            MovieName = findTitle.group(1).strip()
            movies.append((MovieName, linkTag['href']))

    # Fetch TMDB details concurrently while preserving order
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_and_set_tmdb_details, MovieName, href) for MovieName, href in movies]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    results.sort(key= lambda x : x[2], reverse=True)
    # Add directory items in the correct order
    for result in results:
        li, url, _ = result
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
        # li.setInfo('video', {'premiered' : tmdb_details['release_date']})
        release_date = tmdb_details['release_date']
    else:
        # image_url = 'https://luxmovies.live/wp-content/uploads/2024/05/Crew-165x248.jpg'
        release_date = '"1900-01-01"'

    url = build_url({'mode': 'play_movie', 'url': href})
    return li, url, release_date

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


def get_MoviesLink(url):
    MovieQualitySoup = soupObject(url, '.entry-content')
    # start = time.time()
    scriptPattern= r"var url = '([^']+)'"
    # pattern = r'{\d{4}}.+\b1080p\b.+'
    qualityUrl = MovieQualitySoup.select_one('div h5:has(span:-soup-contains("1080p"))').find_next_sibling('p').select_one('a')['href']
    # qualityUrl = MovieQualitySoup.find('span', text=lambda text: text and pattern in text).find_next_sibling('p').select_one('a')['href']
    vcloudSoup = soupObject(qualityUrl)
    VcloudUrl = vcloudSoup.select_one('div.entry-content p a:has(button:-soup-contains("V-Cloud"))')['href']
    playableSoup = soupObject(VcloudUrl, '.card')
    linkJsScript = playableSoup.select('script')[1].text
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


