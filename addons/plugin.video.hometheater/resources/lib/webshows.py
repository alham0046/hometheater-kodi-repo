import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from resources.lib.soupObj import soupObject
import concurrent.futures
import re
import xbmcaddon
import xbmcplugin
import xbmcgui
import xbmc
import sys
from resources.lib import tmdbfetch
import urllib.parse
from resources.lib.impfunctions import build_url, addon_handle, log



webseriesUrl = "https://luxmovies.live"
popularOtts = ['netflix', 'disney', 'hotstar', 'amazon', 'prime', 'sony', 'sonyliv', 'zee', 'zee5', 'jio', 'jiocinema', 'mxplayer']
# DIALOG_PATH = 'special://home/addons/skin.arctic.horizon.2/1080i/WebSeriesView.xml'
ADDON = xbmcaddon.Addon()




def fetch_page_links(page_number, BASE_URL):
    link = f"{BASE_URL}/page/{page_number}"
    response = requests.get(link)
    if response.status_code == 200:
        pages = soupObject(link, '.listing-content')
        return [a for a in pages.select('a') if 'season' in a.get('title').lower()]
    return []

def get_webshowsplatform():
    ottAppsSoup = soupObject(webseriesUrl)
    ottApps = ottAppsSoup.select('div#header-category a span')
    pattern = re.compile(r'^[A-Za-z]')
    for ottApp in ottApps:
        if pattern.match(ottApp.text.strip()) and any(ott in ottApp.text.strip().lower() for ott in popularOtts):
            li = xbmcgui.ListItem(ottApp.text.strip())
            url = build_url({'mode': 'get_webshows', 'url': webseriesUrl + ottApp.parent['href']})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
            # print(ottApp.text.strip())
    
    xbmcplugin.endOfDirectory(addon_handle)

#### this also gives old movies but better as some of new movies appears
def get_webshowsList(url):
    mainCategory = soupObject(url, '.listing-content')
    linkTags = [a for a in mainCategory.select('a') if 'season' in a.get('title').lower()]
    pattern = r"download-(.*?)((season-[1-9]|s[0-1][1-9])|(19[0-9]{2}|20[0-3][0-9])|s[0-1][1-9])"

    # Fetch additional pages concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_page_links, i, url) for i in range(2, 4)]
        for future in concurrent.futures.as_completed(futures):
            linkTags.extend(future.result())

    # List to store movies with their respective URLs
    webSeries = []
    for linkTag in linkTags:
        findTitle = re.search(pattern, linkTag['href'])
        if findTitle:
            # group2 = findTitle.group(2).replace('s0', 'Season') if 's0' in findTitle.group(2) else findTitle.group(2)
            SeriesName = findTitle.group(1).replace('-', ' ').strip()
            webSeries.append((SeriesName, linkTag['href']))

    # Fetch TMDB details concurrently while preserving order
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_and_set_tmdb_details, SeriesName, href) for SeriesName, href in webSeries]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    results.sort(key= lambda x : x[2], reverse=True)
    # Add directory items in the correct order
    for result in results:
        li, url, _ = result
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)

    xbmcplugin.endOfDirectory(addon_handle)

def fetch_and_set_tmdb_details(SeriesName, href):
    li = xbmcgui.ListItem(SeriesName)
    li.setProperty('IsPlayable', 'true')

    # Fetch movie details from TMDB using TMDB Helper
    tmdb_details = tmdbfetch.fetch_tmdb_details_webshows(SeriesName)
    if tmdb_details:
        li.setArt({
            'thumb': tmdb_details['poster_path'],  # Set the thumbnail image
            'icon': tmdb_details['poster_path'],   # Set the icon image (optional)
            'fanart': tmdb_details['backdrop_path']  # Set the fanart image (optional)
        })
        # li.setInfo('video', {'premiered' : tmdb_details['release_date']})
        release_date = tmdb_details['last_season']
    else:
        image_url = 'https://luxmovies.live/wp-content/uploads/2024/05/Crew-165x248.jpg'
        release_date = 1
        # release_date = '"1900-01-01"'

    url = build_url({'mode': 'open_webshow', 'url' : href, 'seriesName': SeriesName, 'lastSeason' : release_date})
    return li, url, release_date

class WebSeriesDialog(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        self.show_data = kwargs['show_data']
        super(WebSeriesDialog, self).__init__()

    def onInit(self):
        xbmc.log("WebSeriesDialog: onInit called", xbmc.LOGDEBUG)
        try:
            self.season_buttons = populate_seasons_and_episodes(self, self.show_data)
            show_season(self, 1, self.show_data)
        except Exception as e:
            xbmc.log(f"WebSeriesDialog: Exception during onInit - {e}", xbmc.LOGERROR)

    def onAction(self, action):
        xbmc.log(f"WebSeriesDialog: onAction called with action_id={action.getId()}", xbmc.LOGDEBUG)
        if action.getId() in [xbmcgui.ACTION_NAV_BACK, xbmcgui.ACTION_PREVIOUS_MENU]:
            self.close()

    def onClick(self, controlId):
        xbmc.log(f"WebSeriesDialog: onClick called with control_id={controlId}", xbmc.LOGDEBUG)
        if controlId in self.season_buttons:
            season_number = self.season_buttons[controlId]
            show_season(self, season_number, self.show_data)

def open_webshow(url, seriesName, lastSeason):
    lastSeason = int(lastSeason)
    show_data = season_Link(lastSeason, url, seriesName)
    open_custom_dialog(show_data)

def open_custom_dialog(show_data):
    addon = xbmcaddon.Addon()
    xml_file = 'WebSeriesView.xml'
    script_path = f"{addon.getAddonInfo('path')}/resources/skins/custom_skin/720p"

    xbmc.log(f"open_custom_dialog: Loading XML file {xml_file} from {script_path}", xbmc.LOGDEBUG)

    dialog = WebSeriesDialog(xml_file, script_path, 'default', '720p', show_data=show_data)
    dialog.doModal()
    del dialog

def populate_seasons_and_episodes(dialog, show_data):
    season_buttons = {}
    
    season_y = 0
    for season_number, episodes in show_data.items():
        button_id = 100 + int(season_number.split(" ")[1])
        list_id = 200 + int(season_number.split(" ")[1])
        xbmc.log(f"populate_seasons_and_episodes: Adding button_id={button_id}, list_id={list_id}", xbmc.LOGDEBUG)
        
        # Add season button
        season_button = xbmcgui.ControlButton(
            50 + (int(season_number.split(" ")[1]) - 1) * 160, 100, 150, 50, f'{season_number}', 'font13', 'font13', 'button-focus.png', 'button-no-focus.png', button_id
        )
        dialog.addControl(season_button)
        season_buttons[int(button_id)] = int(season_number.split(" ")[1])
        
        # Add episodes list
        episode_list = xbmcgui.ControlList(50, 160, 600, 500, 'font13', 'font13', 'button-focus.png', 'button-no-focus.png', list_id)
        for episode in episodes:
            for episodeName, episodeUrl in episode.items():
                list_item = xbmcgui.ListItem(episodeName)
                list_item.setProperty('IsPlayable', 'true')
                list_item.setPath(episodeUrl)
                episode_list.addItem(list_item)
        dialog.addControl(episode_list)
        episode_list.setVisible(False)
    
    return season_buttons

def show_season(dialog, season, show_data):
    xbmc.log(f"show_season: Showing season {season}", xbmc.LOGDEBUG)
    for list_id in range(200, 200 + len(show_data)):
        xbmc.log(f"show_season: Hiding list_id {list_id}", xbmc.LOGDEBUG)
        try:
            dialog.getControl(list_id).setVisible(False)
        except RuntimeError:
            xbmc.log(f"show_season: List ID {list_id} not found", xbmc.LOGERROR)
    try:
        list_id = 200 + season
        xbmc.log(f"show_season: Showing list_id {list_id}", xbmc.LOGDEBUG)
        dialog.getControl(list_id).setVisible(True)
    except RuntimeError:
        xbmc.log(f"show_season: List ID {list_id} not found", xbmc.LOGERROR)



def season_Link(lastSeason, showUrl, seriesName):
    seasonSoup = soupObject(showUrl, ".entry-content ")
    prevSeason = seasonSoup.select_one(f'div.entry-content > h3:-soup-contains("Season {lastSeason - 1}"), div.entry-content > h5:-soup-contains("Season {lastSeason - 1}")')
    if prevSeason:
        prevSeasonTag = prevSeason.find().parent.name
    seasonObj = {}
    seasondict = {}
    futures = []
    if not prevSeason:
        newSoup = soupObject(f"https://dotmovies.autos/?s={seriesName}+season+{lastSeason - 1}", ".inside-article")
        seasonUrl = getvcloudlink(seasonSoup)
        seasonObj[f"Season {lastSeason}"] = {'url' : seasonUrl.find_next_sibling('p').select_one('a:has(button:-soup-contains("V-Cloud"))')['href']}
        for season in range(1, lastSeason):
            log(find=seriesName)
            newUrl = newSoup.select_one(f'h2.entry-title a:-soup-contains("{seriesName.capitalize()}"):-soup-contains("Season {season}")')
            newUrl = newUrl['href'].replace("dotmovies.autos", "luxmovies.live")
            with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures.append(executor.submit(get_Movie_Link, newUrl, season))
        for future in concurrent.futures.as_completed(futures):
            url, sno = future.result()
            seasonObj[f"Season {sno}"] = {'url' : url}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            episodes = [executor.submit(get_EpisodeLink, seasonNo, episodeLink['url']) for seasonNo, episodeLink in seasonObj.items()]
            for episode in concurrent.futures.as_completed(episodes):
                seasonno , res = episode.result()
                seasondict[seasonno] = res                
    else:
        for season in range(1, lastSeason+1):
            seasonUrl = seasonSoup.select_one(f'div.entry-content > {prevSeasonTag}:-soup-contains("Season {season}"):-soup-contains("1080p")')
            seasonObj[f"Season {season}"] = {'url' : seasonUrl.find_next_sibling('p').select_one('a')['href']}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            episodes = [executor.submit(get_EpisodeLink, seasonNo, episodeLink['url']) for seasonNo, episodeLink in seasonObj.items()]
            for episode in concurrent.futures.as_completed(episodes):
                seasonno , res = episode.result()
                seasondict[seasonno] = res

    return seasondict


def get_EpisodeLink(season_Number, episode_link):
    vcloudSoup = soupObject(episode_link)
    VcloudUrls = vcloudSoup.select('div.entry-content p a:has(button:-soup-contains("V-Cloud"))')
    with concurrent.futures.ThreadPoolExecutor() as executor:
        episodes = [executor.submit(episode_playable, episode['href'], episodeNo+1) for episodeNo, episode in enumerate(VcloudUrls)]
        results = [future.result() for future in concurrent.futures.as_completed(episodes)]
    return season_Number, results

def getvcloudlink(soup):
    hrtags = soup.select_one(f'div.entry-content>hr').find_next_siblings()
    reqtag = next(tag for tag in hrtags if "1080" in tag.text)
    return reqtag            

def episode_playable(episode_Link, episode_No):
    scriptPattern= r"var url = '([^']+)'"
    vcloudSoup = soupObject(episode_Link, '.card')
    vcloudUrl = vcloudSoup.select('script')[1].text
    playableUrl = re.search(scriptPattern, vcloudUrl).group(1)
    # print(playableUrl)
    mp4Soup = soupObject(playableUrl)
    mp4arr = mp4Soup.select('a[href$=".mkv"], a[href$=".mp4"], a[href$=".avi"] ')
    if len(mp4arr) > 0:
        mp4Url = mp4arr[0]['href']
        return {f'Episode {episode_No}' : mp4Url}
    elif "gofile" in mp4Soup.get_text().lower() :
        gofileUrl = mp4Soup.select_one('a[href*="gofile"]')['href']
        gofileReq = requests.get(gofileUrl)
        gofileSoup = BeautifulSoup(gofileReq.text, 'html.parser')
        mp4Url = gofileSoup.select_one('meta[content*="https"]')['content'].replace("store2", "file5").replace("thumb_", "").replace(".jpg", "")
        return {f'Episode {episode_No}' : mp4Url}
    elif "PixeLServer".lower() in mp4Soup.get_text().lower() :
        mp4Url = mp4Soup.select_one('a[href*="pixeldra"]')['href']
        return {f'Episode {episode_No}' : mp4Url}


def get_Movie_Link(url, season):
    soup = soupObject(url)
    vcloud_Link = getvcloudlink(soup)
    return vcloud_Link.find_next_sibling('p').select_one('a:has(button:-soup-contains("Download Now")), a:has(button:-soup-contains("V-Cloud"))')['href'], season



# def open_custom_dialog(show_data):
#     addon = xbmcaddon.Addon()
#     xml_file = 'WebSeriesView.xml'
#     script_path = addon.getAddonInfo('path') + '/resources/skins/custom_skin/720p/'
#     dialog = xbmcgui.WindowXMLDialog(xmlFilename=xml_file, scriptPath=script_path)

#     dialog.show()
#     season_buttons = populate_seasons_and_episodes(dialog, show_data)
#     show_season(dialog, 1, show_data)
    
#     while True:
#         action = dialog.getAction()
#         if action.getId() in season_buttons:
#             season_number = season_buttons[action.getId()]
#             show_season(dialog, season_number, show_data)
#         if action.getId() in [xbmcgui.ACTION_NAV_BACK, xbmcgui.ACTION_PREVIOUS_MENU, xbmcgui.ACTION_CLOSE_DIALOG]:
#             break
    
#     dialog.close()

# def fetch_season_and_episode_data(webshow_url):
#     # Implement your logic to fetch season and episode data
#     # Return a dictionary with season numbers as keys and lists of episodes as values
#     # For example:
#     # {
#     #     1: [{'title': 'Episode 1'}, {'title': 'Episode 2'}],
#     #     2: [{'title': 'Episode 1'}, {'title': 'Episode 2'}],
#     #     3: [{'title': 'Episode 1'}, {'title': 'Episode 2'}]
#     # }
#     pass


# def play_webshow(video_url):
#     # test_link = get_cached_link(video_url)
#     # if not test_link:
#     test_link = get_ShowLink(video_url)
#         # save_to_cache(video_url, test_link)
#     li = xbmcgui.ListItem(offscreen = True)
#     li.setPath(test_link)
#     # player = xbmc.Player()
#     # player.play(test_link, listitem=li)
#     xbmcplugin.setResolvedUrl(addon_handle, True, listitem=li)
