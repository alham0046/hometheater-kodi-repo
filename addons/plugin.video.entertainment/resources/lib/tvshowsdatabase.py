from resources.lib.soupObj import soupObject
from resources.lib.impfunctions import addon_handle, build_url, log
from resources.lib.urlResolver import resolve_url
from resources.utils.db_util import getdb, tvCache, tvEpisodeCache, updateDatabase
import xbmcplugin
import re
import xbmcgui
import xbmc
import os
import concurrent.futures
import requests
from dateutil import parser
import threading
from resources.lib.tvShows import get_VideoLink
import pymongo

urlmain = "https://www.yodesitv.info/"
channelList = ["star plus", "sony tv", "star bharat", "zee tv", "colors", "sab tv"]

def mongoConnect(dbname, collection = None):
    connectdb = pymongo.MongoClient(f"mongodb://alham0046:alham789@ac-2ybb09o-shard-00-00.odsdwox.mongodb.net:27017,ac-2ybb09o-shard-00-01.odsdwox.mongodb.net:27017,ac-2ybb09o-shard-00-02.odsdwox.mongodb.net:27017/?ssl=true&replicaSet=atlas-vwia5y-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0/{dbname}")
    if connectdb:
        print("connection success")
        if not collection:
            return connectdb[dbname]
        elif collection:
            if collection not in connectdb[dbname].list_collection_names():
                return None
            return connectdb[dbname][collection]
        
# hometheater_showList = mongoConnect("Hometheater", "ShowsList")



def get_channel():
    for channel in channelList:
        churl = "-".join(channel.split(" ")) if (" " in channel) else channel
        li = xbmcgui.ListItem(channel.upper())
        url = build_url({'mode': 'get_shows', 'url': urlmain + churl})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    # li = xbmcgui.ListItem("Airing Today")
    # url = build_url({'mode': 'airing_shows', 'url': channel.find('a').get('href')})
    # xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

def get_shows(showurl):
    channelName = " ".join(showurl.split("/")[-1].split("-")).upper()
    showLists = getdb(dbname="tvCache.db", tablename="TVshowCache", condition=channelName, whereclause="Channel_Name", orderby="Show_Status, Show_Name")
    log(message="The showlist is", find=showLists)
    def setShowDetails(showLists):
        for showList in showLists:
            _,title, poster, backdrop, url, show_status = showList.values() if isinstance(showList, dict) else showList
            # log(find=title)
            li = xbmcgui.ListItem(title)
            li.setArt({
                'thumb' : poster,
                'icon' : poster,
                'fanart' : backdrop
            })
            if show_status == "Airing":
                li.addContextMenuItems([("Completed", f'RunPlugin({build_url({"mode": "set_status", "showname": title, "status": "Completed"})})')])
            elif show_status == "Completed":
                li.addContextMenuItems([("Airing", f'RunPlugin({build_url({"mode": "set_status", "showname": title, "status": "Airing"})})')])
            showurl = build_url({'mode': 'get_Episodes', 'url': url})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=showurl, listitem=li, isFolder=True)
        xbmcplugin.endOfDirectory(addon_handle)
        if isinstance(showLists[0], tuple) :
            episodeList([(val[1],val[4]) for val in showLists if val[0] == channelName and val[5] == "Airing"], channelName)
        elif isinstance(showLists[0], dict):
            episodeList([(val["showname"],val["url"]) for val in showLists if val["chname"] == channelName], channelName)

    if showLists:
        setShowDetails(showLists)
    elif not showLists:
        showLists = tvshow(showurl)
        setShowDetails(showLists)

def set_status(showname, status):
    updateDatabase(dbname="tvCache.db", tablename="TVshowCache", updatevar="Show_Status", updatevalue=status, whereclause="Show_Name", condition=showname)
    # xbmc.executebuiltin('Container.Refresh')
    

def tvshow(url):
    # url = "https://www.yodesitv.info/star-plus"
    # shows = soupObject(url, '#tab-0-title-1')
    # showLists = shows.find_all('div', attrs={'class': re.compile('^one_')})
    hometheater_showList = mongoConnect("Hometheater", "ShowsList")
    showLists = [showlist for showlist in hometheater_showList.find({}, {'_id' : 0})]
    channelDetail = []
    for showList in showLists:
        chname, showname, poster, backdrop, showurl, showstatus = showList.values()
        chdet = {}
        chdet["chname"] = chname
        chdet["showname"] = showname
        chdet["poster"] = poster
        chdet["backdrop"] = backdrop
        chdet["url"] = showurl
        chdet["Show_Status"] = showstatus
        channelDetail.append(chdet)
        # print(showList.text)
    # print(channelDetail)
    tvCache(channelDetail)
    return channelDetail


def episodeList(episodeUrlList, channelName):
    hometheater_episodeList = mongoConnect("Hometheater", "episodeList")
    if hometheater_episodeList is not None:
        showlistsmongodata = [data for data in hometheater_episodeList.find({'channelName' : channelName}, {"_id" : 0}).sort({'episodeDate' : -1})]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        if hometheater_episodeList is not None:
            futures = [executor.submit(episodePage, episodeUrl, channelName, showname, [episodemongo for episodemongo in showlistsmongodata if episodemongo['showName'] == showname]) for showname, episodeUrl in episodeUrlList]
        else:
            futures = [executor.submit(episodePage, episodeUrl, channelName, showname) for showname, episodeUrl in episodeUrlList]
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                log(message="the object to be added is", find=future.result())
                tvEpisodeCache(future.result())

def get_Episodes(url):
    showname = " ".join(url.split("/")[-2].split("-")).title()
    episodesdb = getdb(dbname="tvEpisodes.db", tablename="tvEpisodes", whereclause="Show_Name", condition=showname, orderby="Episode_Date DESC")
    for episode in episodesdb:
        chname, shname, _, title, imgurl, episodeUrl = episode
        li = xbmcgui.ListItem(title)
        li.setArt({
            'thumb' : imgurl,
            'icon' : imgurl,
            'fanart' : imgurl
        })
        li.setProperty('IsPlayable', 'true')
        epiUrl = build_url({'mode': 'play_video', 'url': episodeUrl})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=epiUrl, listitem=li, isFolder=False)
    xbmcplugin.endOfDirectory(addon_handle)

def play_video(episodeUrl):
    li = xbmcgui.ListItem(offscreen = True)
    li.setPath(episodeUrl)
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=li)



    
    # items = []
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     futures = [executor.submit(episode_img, episode) for episode in episodes]
    #     results = [future.result() for future in concurrent.futures.as_completed(futures)]
    # results.sort(key= lambda x : x[2], reverse=True)
    # print(results)
    # for result in results:
    #     title, img, _ = result
    #     episodeDetail = {}
    #     episodeDetail["showname"] = " ".join(episodeUrl.split("/")[-2].split("-")).title()
    #     episodeDetail["title"] = title
    #     episodeDetail["img"] = img
    #     items.append(episodeDetail)
    # tvEpisodeCache(items)

def episodePage(episodeUrl, channelname, showname, showlistsmongodata = None):
    episodeDetail = []
    # showname = " ".join(episodeUrl.split("/")[-2].split("-")).title()
    showlistdb = getdb(dbname="tvEpisodes.db", tablename="tvEpisodes", condition=showname, whereclause="Show_Name" , select="Episode_Title, Episode_Date")
    showlistdatedb = [date[1] for date in showlistdb]
    showlistdbtitles = [entry[0] for entry in showlistdb]
    from datetime import datetime
    if str(datetime.today().date()) not in showlistdatedb:
        if showlistsmongodata:
            for showlistmongodata in showlistsmongodata:
                if showlistmongodata['episodeTitle'] in showlistdbtitles:
                    # log(message="breaking show", find=episode.text)
                    break
                else:
                    chname, shname, title, img, date, url = showlistmongodata.values()
                    # epidet = appendepisodes(showlistmongodata['channelName'], showlistmongodata['showName'], showlistmongodata['episodeTitle'], showlistmongodata['episodeImg'], showlistmongodata['episodeDate'], showlistmongodata['episodeUrl'])
                    epidet = appendepisodes(chname, shname, title, img, date, url)
                    episodeDetail.append(epidet)
            log(message="the episode list is", find=episodeDetail)
            return episodeDetail
        else:
            return None
            log(message="moving out of mongodb", find=showname)
            episodeSoup = soupObject(episodeUrl, '#content_box')
            episodes = episodeSoup.select('h2.front-view-title')
            # showlistdb = getdb(dbname="tvEpisodes.db", tablename="tvEpisodes", condition=showname, whereclause="Show_Name" , select="Episode_Title")
            # log(find=showlistdb)
            for episode in episodes:
                # log(episode.text)
                if episode.text.strip() in showlistdbtitles:
                    log(message="breaking show", find=episode.text)
                    break
                else:
                    log(message="new episode adding", find=episode.text)
                    # epidet = {}
                    videoLinkSoup = soupObject(episode.find('a')['href'], '.thecontent')
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        imgPath = executor.submit(episode_img, videoLinkSoup).result()
                        urlPath = executor.submit(getEpisodeUrl, episode.find('a')['href']).result()
                    # imgPath = episode_img(episode)
                    pattern = r"\d{1,2}(th|st|nd|rd) [A-Za-z]+ \d{4}"
                    matching = re.search(pattern, episode.text.strip()).group()
                    formattedDate = re.sub(r'(\d{1,2})(st|nd|rd|th)', r'\1', matching)
                    airingDate = parser.parse(formattedDate, dayfirst=True).date()
                    epidet = appendepisodes(channelname, showname, episode.text, imgPath, airingDate, urlPath)
                    # epidet["channelname"] = channelname
                    # epidet["showname"] = showname
                    # epidet["title"] = episode.text
                    # epidet["img"] = imgPath
                    # epidet["episodedate"] = airingDate
                    # epidet["EpisodeUrl"] = urlPath
                    # tvEpisodeCache([epidet])
                    episodeDetail.append(epidet)
            return episodeDetail
        

    else:
        log(message="skipped successfully", find=showname)
        return None
    
    # Fetch images in the background

def appendepisodes(channelname, showname, episode, imgPath, airingDate, urlPath):
    epidet = {}
    epidet["channelname"] = channelname
    epidet["showname"] = showname
    epidet["title"] = episode
    epidet["img"] = imgPath
    epidet["episodedate"] = airingDate
    epidet["EpisodeUrl"] = urlPath
    return epidet
    

# def episode_img(episode):
# def episode_img(videoLinkSoup):
#     # videoLinkSoup = soupObject(episode.find('a')['href'], '.thecontent')
#     links = videoLinkSoup.select_one('span:-soup-contains("VKprime")')
#     if links:
#         validVkprime = links.parent.find_next_sibling('p').select_one('a')['href']
#         linkSoup = soupObject(validVkprime, '#content')
#         iframe = linkSoup.select_one('iframe').get('src')
#         imgId = iframe.split("embed-")[1].split(".")[0]
#         imgUrl1 = f"https://ovhprime0.vkcdn5.com/i/01/00175/{imgId}.jpg"
#         imgUrl2 = f"https://ovhprime111.vkcdn5.com/i/01/00175/{imgId}.jpg"
#         imgUrl3 = f"https://sys.vkcdn5.com/i/01/00175/{imgId}.jpg"
#         imgUrl4 = "https://{prefix}.vkcdn5.com/i/01/{id}/{imgId}.jpg"
#         if requests.get(imgUrl1).status_code == 200:
#             imgval = imgUrl1
#         elif requests.get(imgUrl2).status_code == 200:
#             imgval = imgUrl2
#         elif requests.get(imgUrl3).status_code == 200:
#             imgval = imgUrl3
#         else:
#             prefixes = ["ovhprime0", "ovhprime111", "sys"]
#             urlids = ["00174", "00173", "00172", "00171"]
#             imgval = ""
#             for prefix in prefixes:
#                 for urlid in urlids:
#                     tryimgurl = imgUrl4.format(prefix = prefix, id = urlid, imgId=imgId)
#                     if requests.get(tryimgurl).status_code == 200:
#                         imgval = tryimgurl
#                         break
#     else:
#         imgval = ""
    
#     # Update the list item in Kodi
#     return imgval


# def getEpisodeUrl(videoLinkSoup):
#     return get_VideoLink(videoLinkSoup)