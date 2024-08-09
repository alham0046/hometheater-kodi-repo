# import base64
# import urllib.parse

# # Example JavaScript object values
# cf_chl_opt = {
#     'cvId': '3',
#     'cZone': "luxmovies.live",
#     'cType': 'managed',
#     'cNounce': '96371',
#     'cRay': '8a93e3d10a316017',
#     'cHash': 'd99ea1454b731df',
#     'cUPMDTk': "/?s=mirzapur&__cf_chl_tk=_RzS1cGqsCCF6eAEwILUCbtjhg4JXVqgecuCx36IMaU-1721991667-0.0.1.1-3711",
#     'cFPWv': 'g',
#     'cTTimeMs': '1000',
#     'cMTimeMs': '390000',
#     'cTplV': 5,
#     'cTplB': 'cf',
#     'cK': "",
#     'fa': "/?s=mirzapur&__cf_chl_f_tk=_RzS1cGqsCCF6eAEwILUCbtjhg4JXVqgecuCx36IMaU-1721991667-0.0.1.1-3711",
#     'md': "JOhebRCW2AsfYxDMmQrjryu4u_uiEe4HlxT_E0eRjok-1721991667-1.1.1.1-nhgxpP6fuhLMA.QwtMWxXf4elDhk9QnhT9R2RCaKSduclvqkTWNUqm2oydNzNoMGJjpiG6hfWBK060TGubH08LM.hEqZ_FSQvmJPx_96WhqOjP8roHEtDEgJfcPGoOdi4NZAHT7uxiAuEDx4zNif_WnPx.R6CRCG.qfW4YEA_ZA8rPRowbTr_otAjVPhzgyKaWpTg3MIeT8sSTE_JCkwvIm_VxlzzQg0sY_.M.x65kQheBKaUgTJyVt9_UDR9gIH3gjbOY3umgNN1rJM_05JK4YUnXekLCcz2L9Yoil1Rjj3uwTpUu_y5qo4eJbPIkLQPy32Kpw81PfvhS0bEpDeGQD8cqls3G0S6n4R3rg1ugRXS3sKro9j7DP85xHfyrC2wU.xYinsoTbcx2BLPzd4EDARRX9.MCJh7p6fml5p4NiFhiPtBEu8nb2H1ZMEwcXBeoJ3y9BS9PXHd907hhFT63SEEICu8edJ7ULvLDcwnmDX0qXSklFlWpd9odEyGWSjEvpiKRvdFE6kuaWq7_5AeJjerLhjn_EvatAUWAd_6tDD2Iu3Qrw9sKHJV5d.8oJkWmghvv4lcBKxr.dG9Kj4DQ1Ooz6vj0WfvZalKRKSPlIWF9Vofdplh5Xgtp5HohOA821j1vzzQUZCZkTlsg3Y.lQQv_sU15SROTWV8J45hXGdcvPecE6FBf3o8EObzE0k7hby95hNQJRYCL8MD3EhMCyKjihn6gXaCNLw9OMkIM1OyKTomEZDGfY86uBekTCUyBu169eIx4bLslmLQy4TdcPxJueiwhJxXce2RdYnafcB6K_k7PtbGI2k5wTNdC6t2avdiWBM_DxQcLR4yH1N3dUBo_PgDS7Mv8rHTCWHPyN4FGPtEejBUcmH8tOJix0MOcNdyyy3jvPAP_.1Nr.g.px_XI9c1RujGapR5mIhuIgP8Z3RkT97fN5RBMJRVYescCxmAvbCykllNkLUvUCroZJ88NBrp1e4U28maoodMDEtyGjnyoZi_n028tD1.NsTFVMUZ668rIdvllEozgwrtBdqSJisr.0uJz7ZMfgidZ8irTN3150CjSh9gLi2hS0zNDgLCqXY5tlGcawKLXdYE2mdTJvPn.iTzK8ibBGElWbZUHVpEb47IRc.4v5Jm1RFBG5UZBIiJeD1AZxe_4C2oRMDkMrdr6v2C3gyuaePVqoOBJA8jTQGdmFNC6_rNt0ibeu1SeM7pBGj2dHQenaoZEkMRg_o7RlE9k9C1OEHIyh3EzN81.Gr1wyndvElLIuNapI9wVOKey3n3DjRZHJ.p4H_wvsY5wAva_5thnwRGFJp..vkmEWqMmlHxPWH_DrrKKDH_RB3DlIzahw_0IufzcQb5kf5UMf8Qv4NxwSEngbp.Fk_V7NgaN74nl0_nnvljjoE2p4WhDlM9VERHuAcoUfr66J7UYwa.jmemD6ztCQ",
#     'mdrd': "jIT_qx.YUt94rLH0hm_iztIwZMAEf0Hq4Dr1ia_o8XE-1721991667-1.1.1.1-68x4Q8wLskKHBlLOFCd8bADqJtKB9UqhRHlCHiHxBLQfOjJBn0IF3hJi5C2pVyKrqbwLAQhjkU0QJrMOLr3OZ8vnFX08xj6I32chFQqywoPztP5tw7OyEm3O9qFafOw0rREgPrIG4ss4C4.bAXfEDV_gfsiQ1Ju5KCR54ncQuhv60NATaubNgOLosDUnU37tqbPPeIrr9NAr9AVMyScvVA8L50odUyh.KaTIsGKVO5rvw1_p5yDvGPVm2RN3RMeEllbjFOyK22telmC_CHsZSFJOL3zX87MVF6ivYafLYLQ_GWJwlIHLVVXgEoNJH6HbfVvCQj18XG1kJZARU0hdwt.4b.IbgKyiultL1RLYqShdRQffXpRSFGVK6WUthBrh9LkDaQSmmwwBBrtpjbF.RYWuc5MPyboqeylKKlTy9Djd7m5_bcGyZ8LuaOPBIPu96fTTclDzl7BoA4nnq0hyi5d.IUSYfbA59ksnThbNczkMgV15lPaVXn1d8EdTOMrn07tkIVHl7aSLMbyBaUNZ7G01xRf4Jv8.tzIvJRg6jfYbhFhrKkI4vf3TuEFznInmhrjOkyb0xvG1wbUyXIhFXCTOXjWaZK8f00V1L_gepA4vNL2oW7jajhMkBdU2Yd0ewETWKMzUHYbE5CjcoiOpAsAsjIXGmP1.xXC30.9IiQktSmZLXT7FCb0J6errPZXP2KcJKzvWyWchKeCj0HhUVFyeXye3kL4dBa42ScMoyykR62tn4L.wms_UPJ3CAU25Dn8LgNd.2vZXiHnIfi.PPsRW.G3keI6gWK7N4sTmLp7DIT1yAnYoELn87VwtwZeymuiwOxU5.rQnTbn.xI8G3V._zQD6NI4kQliSU68PSbwlEqi.6VyzMnQlJgV0bwz31IDrsGyy3pynSP.1GEYeoZqPYRTc7tF8KbcH2tl0r4hZoiRh5iNOsBUtAGhz2kkwr5kh5QMAc.XAKkZ06RVRK.B3LItHEqmkQEvDLcBYmbdVo3ULH5omE6GpH_dYNJGi53XfHkXTtWbcWf8Uo5mUOTBrz.ZSsdphFdlWBoZZ8y_NXUBDxtq0HDiQs5nd84HRifY.Eg46N4mWx4Of7blRYr5jKDgfk8x5wVDmSP1yPB5X3F1U8Ah4i7hURx_9uj9chWsn7uqnpG6_QSYMsPPBO_baY9F8dFURs8krsw5EGyM3BWESQk6u_JmW3t08PKMeOJr5.CaE6BFbny9cV4uAoi0M2pO1_iqLsfdXEGTiyK0xN3thDpVKaCQ1iBMS_j5lK7RmHskwGMKfaD.N2u0TpmR9Wj7lVbGg8xtMUk6VGRReQz18SO5UlVPZr92OKRxM_XfbUegTExvDp4K97XuRznAjGLrwwscL4FvZnQ3xi47S6aeD2iD7JmtGXMZLs2PBvOuzP0PjYAY_AtNsA2qqyqT.OtrcQdDq6VesIjkfpjGAO9uoJXhUEoBbDa9SKS8H5wNTK9HnQuOV9",
#     'nv': '1',
#     's': '73ba558274ff7e50c07d9038353c53b77b49816402e16396fca01c57350e9ba8',
#     'f': 'jpg',
#     'id': '63e3ac721a80bfa57687a37a',
#     'ru': "aHR0cHM6Ly9sdXhtb3ZpZXMubGl2ZS9zdHJlYW0vYXhIUnJLVXlDV2k4N3AwcjFOSldPUEJHaTBHUER4U1A1cW5oY1g0NTcyTEhxUlhRQmtzdnlSNnN3YlRBMVpkbkYxWkhodFpqdGpUUGMzN0pJaS9NUUR1MkhLT0d4dU9sMGJJU0M4SHBHZjQvWVpWbklUbUZwNEw5RlVwWWw0QkhBNzJPdE5TMEU1UVYvWExORVkwd01PbVJoTnd5RWFXV3oydnF6VHRHMlUvcnEzMkp4WGFSdGJVMHFYYUNJREJHNTB3PT0=",
#     'ra': "WnVnY1RzSUE=",
#     't': 'mjs'
# }

# def construct_url(cf_chl_opt):
#     ru_encoded = cf_chl_opt['ru']
#     ru_decoded = base64.b64decode(ru_encoded).decode('utf-8')
#     return ru_decoded

# # Constructed URL
# url = construct_url(cf_chl_opt)
# print(url)


# exit()

import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import re
import time
from resources.lib.soupObj import soupObject
import concurrent.futures
import asyncio
from fp.fp import FreeProxy
from dateutil import parser
import os

# def get_moviesList(url):
#     mainCategory = soupObject(url, '.listing-content')
#     linkTags = [a for a in mainCategory.select('a') if 'season' not in a.get('title').lower()]
#     # print(linkTags)
#     pattern = r"Download (.*?) \((19[0-9]{2}|20[0-3][0-9])"

#     # Fetch additional pages concurrently
#     # with concurrent.futures.ThreadPoolExecutor() as executor:
#     #     futures = [executor.submit(fetch_page_links, i, url) for i in range(2, 4)]
#     #     for future in concurrent.futures.as_completed(futures):
#     #         linkTags.extend(future.result())

#     # List to store movies with their respective URLs
#     movies = []
#     for linkTag in linkTags:
#         findTitle = re.search(pattern, linkTag["title"])
#         # print(findTitle)
#         if findTitle:
#             MovieName = findTitle.group(1).strip()
#             print(MovieName.split(" – ")[0].strip())
#             # movies.append((MovieName, linkTag['href']))

# # get_moviesList("https://luxmovies.live/category/web-series/netflix/")

# def get_ShowLink2(url):
#     start = time.perf_counter()
#     ShowQualitySoup = soupObject(url)
#     # start = time.time()
#     scriptPattern= r"var url = '([^']+)'"
#     # pattern = r'{\d{4}}.+\b1080p\b.+'
#     qualityUrl = ShowQualitySoup.select_one('div.entry-content h3:has(span:-soup-contains("1080p"))')
#     if qualityUrl:
#         qualityUrl = qualityUrl.find_next_sibling('p').select_one('a')['href']
#     else:
#         qualityUrl = "no data found"
#     print(qualityUrl)
#     end = time.perf_counter()
#     print(end-start)
# def get_ShowLink(url):
#     start = time.perf_counter()
#     ShowQualitySoup = soupObject(url)
#     # start = time.time()
#     scriptPattern= r"var url = '([^']+)'"
#     # pattern = r'{\d{4}}.+\b1080p\b.+'
#     qualityUrl = ShowQualitySoup.find(lambda tag: get_tag(tag, "h3", [f"Season {3}", "1080p"]))
#     if qualityUrl:
#         qualityUrl = qualityUrl.find_next_sibling('p').select_one('a')['href']
#     else:
#         qualityUrl = "no data found"
#     print(qualityUrl)
#     end = time.perf_counter()
#     print(end-start)
# def get_ShowLink3(url):
#     start = time.perf_counter()
#     ShowQualitySoup = soupObject(url)
#     # start = time.time()
#     scriptPattern= r"var url = '([^']+)'"
#     prevSeason = ShowQualitySoup.select(f'div.entry-content > h3:-soup-contains("Season 2")')
#     if prevSeason:
#         print(prevSeason)
#     # pattern = r'{\d{4}}.+\b1080p\b.+'
#     seasonobj = {}
#     for season in range(3):
#         qualityUrl = ShowQualitySoup.select_one(f'div.entry-content > h3:-soup-contains("Season {season+1}"):-soup-contains("1080p")')
#         if qualityUrl:
#             seasonobj[f"season {season +1}"] = qualityUrl.find_next_sibling('p').select_one('a')['href']
#         else:
#             seasonobj[f"season {season +1}"] = "no data found"
#     print(seasonobj)
#     end = time.perf_counter()
#     print(end-start)

# def get_tag(tag, tag_name, search_text):
#     # return tag.name == 'span' and 'Netflix' in tag.text
#     return tag.name == tag_name and all(word in tag.text for word in search_text)


# def season_Link(lastSeason, showUrl, seriesName):
#     start = time.perf_counter()
#     seasonSoup = soupObject(showUrl, ".entry-content ")
#     prevSeason = seasonSoup.select_one(f'div.entry-content > h3:-soup-contains("Season {lastSeason - 1}"), div.entry-content > h5:-soup-contains("Season {lastSeason - 1}")')
#     print(type(lastSeason))
#     if prevSeason:
#         prevSeasonTag = prevSeason.find().parent.name
#     seasonObj = {}
#     seasondict = {}
#     futures = []
#     if not prevSeason:
#         newSoup = soupObject(f"https://dotmovies.autos/?s={seriesName}+season+{lastSeason - 1}", ".inside-article")
#         # seasonUrl = seasonSoup.select_one(f'div.entry-content span:-soup-contains("1080p")').parent.parent
#         seasonUrl = getvcloudlink(seasonSoup)
#         seasonObj[f"Season {lastSeason}"] = {'url' : seasonUrl.find_next_sibling('p').select_one('a:has(button:-soup-contains("V-Cloud"))')['href']}
#         for season in range(1, lastSeason):
#             newUrl = newSoup.select_one(f'h2.entry-title a:-soup-contains("{seriesName}"):-soup-contains("Season {season}")')
#             newUrl = newUrl['href'].replace("dotmovies.autos", "luxmovies.live")
#             with concurrent.futures.ThreadPoolExecutor() as executor:
#                     futures.append(executor.submit(get_Movie_Link, newUrl, season))
#         for future in concurrent.futures.as_completed(futures):
#             url, sno = future.result()
#             seasonObj[f"Season {sno}"] = {'url' : url}
#         with concurrent.futures.ThreadPoolExecutor() as executor:
#             episodes = [executor.submit(get_EpisodeLink, seasonNo, episodeLink['url']) for seasonNo, episodeLink in seasonObj.items()]
#             for episode in concurrent.futures.as_completed(episodes):
#                 seasonno , res = episode.result()
#                 seasondict[seasonno] = res
            

#         print("this is if part")
#     else:
#         print("this is else part")
#         for season in range(1, lastSeason+1):
#             seasonUrl = seasonSoup.select_one(f'div.entry-content span:-soup-contains("Season {season}"):-soup-contains("1080p")').parent.parent
#             seasonObj[f"Season {season}"] = {'url' : seasonUrl.find_next_sibling('p').select_one('a')['href']}
#         with concurrent.futures.ThreadPoolExecutor() as executor:
#             episodes = [executor.submit(get_EpisodeLink, seasonNo.split(" ")[1], episodeLink['url']) for seasonNo, episodeLink in seasonObj.items()]
#             for episode in concurrent.futures.as_completed(episodes):
#                 # print("vcloud url is : ", episode.result())
#                 seasonno , res = episode.result()
#                 seasondict[seasonno] = res
#     print(seasondict)


#     print(seasonObj)
#     end = time.perf_counter()
#     print("Time taken is : ", end-start)

# def get_Movie_Link(url, season):
#     print(season)
#     soup = soupObject(url)
#     vcloud_Link = getvcloudlink(soup)
#     return vcloud_Link.find_next_sibling('p').select_one('a:has(button:-soup-contains("Download Now")), a:has(button:-soup-contains("V-Cloud"))')['href'], season

# def getvcloudlink(soup):
#     hrtags = soup.select_one(f'div.entry-content>hr').find_next_siblings()
#     reqtag = next(tag for tag in hrtags if "1080" in tag.text)
#     return reqtag


# def get_EpisodeLink(season_Number, episode_link):
#     vcloudSoup = soupObject(episode_link)
#     VcloudUrls = vcloudSoup.select('div.entry-content p a:has(button:-soup-contains("V-Cloud"))')
#     # print(VcloudUrls)
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         episodes = [executor.submit(episode_playable, episode['href'], episodeNo+1) for episodeNo, episode in enumerate(VcloudUrls)]
#         results = [future.result() for future in concurrent.futures.as_completed(episodes)]
#     return season_Number, results
            

#     # return {season_Number : VcloudUrls}

# def episode_playable(episode_Link, episode_No):
#     scriptPattern= r"var url = '([^']+)'"
#     vcloudSoup = soupObject(episode_Link, '.card')
#     vcloudUrl = vcloudSoup.select('script')[1].text
#     playableUrl = re.search(scriptPattern, vcloudUrl).group(1)
#     # print(playableUrl)
#     mp4Soup = soupObject(playableUrl)
#     mp4arr = mp4Soup.select('a[href$=".mkv"], a[href$=".mp4"], a[href$=".avi"] ')
#     if len(mp4arr) > 0:
#         mp4Url = mp4arr[0]['href']
#         return {f'Episode {episode_No}' : mp4Url}
#     elif "gofile" in mp4Soup.get_text().lower() :
#         gofileUrl = mp4Soup.select_one('a[href*="gofile"]')['href']
#         gofileReq = requests.get(gofileUrl)
#         gofileSoup = BeautifulSoup(gofileReq.text, 'html.parser')
#         mp4Url = gofileSoup.select_one('meta[content*="https"]')['content'].replace("store2", "file5").replace("thumb_", "").replace(".jpg", "")
#         return {f'Episode {episode_No}' : mp4Url}
#     elif "PixeLServer".lower() in mp4Soup.get_text().lower() :
#         mp4Url = mp4Soup.select_one('a[href*="pixeldra"]')['href']
#         return {f'Episode {episode_No}' : mp4Url}



    # print(reqtag)
    # return soup.select_one(f'div.entry-content span:-soup-contains("1080p"):-soup-contains("Season {season}")').parent.parent.find_next_sibling('p').select_one('a')['href'], season
# def season_Link(lastSeason, showUrl, seriesName):
#     start = time.perf_counter()
#     seasonSoup = soupObject(showUrl, ".entry-content ")
#     prevSeason = seasonSoup.select(f'div.entry-content > h3:-soup-contains("Season {lastSeason - 1}")')
#     seasonObj = {}
#     futures = []
#     if not prevSeason:
#         newSoup = soupObject(f"https://dotmovies.autos/?s={seriesName}+season+{lastSeason - 1}", ".inside-article")
#     for season in range(1, lastSeason+1):
#         if (lastSeason == season) or prevSeason:
#             seasonUrl = seasonSoup.select_one(f'div.entry-content > h3:-soup-contains("Season {season}"):-soup-contains("1080p")')
#             seasonObj[f"Season {season}"] = seasonUrl.find_next_sibling('p').select_one('a')['href']
#         # seasonUrl = seasonSoup.select_one(f'div.entry-content > h3:-soup-contains("Season {season}"):-soup-contains("1080p")')
#         # if seasonUrl:
#         #     seasonObj[f"Season {season}"] = seasonUrl.find_next_sibling('p').select_one('a')['href']
#         else:
#             newUrl = newSoup.select_one(f'h2.entry-title a:-soup-contains("{seriesName}"):-soup-contains("Season {season}")')
#             newUrl = newUrl['href'].replace("dotmovies.autos", "luxmovies.live")
#             with concurrent.futures.ThreadPoolExecutor() as executor:
#                 futures.append(executor.submit(get_Movie_Link, newUrl, season))
#     for future in concurrent.futures.as_completed(futures):
#         url, sno = future.result()
#         seasonObj[f"Season {sno}"] = url

#     print(seasonObj)
#     end = time.perf_counter()
#     print("Time taken is : ", end-start)



# get_ShowLink3("https://luxmovies.live/download-mirzapur-s03-complete-hindi-web-series-480p-720p-1080p-2160p-web-dl-prime-video/")
# season_Link(3, "https://luxmovies.live/download-kota-factory-season-3-hindi-480p-720p-1080p-netflix-original/", "Kota Factory")
# season_Link(3, "https://luxmovies.live/download-mirzapur-s03-complete-hindi-web-series-480p-720p-1080p-2160p-web-dl-prime-video/", "Mirzapur")
# season_Link(3, "https://luxmovies.wiki/download-aarya-season-3-hindi-hotstar-specials-complete-series-480p-720p-1080p/", "Aarya")

def episodeList(episodeUrl):
    episodeSoup = soupObject(episodeUrl, '#content_box')
    episodes = episodeSoup.select('h2.front-view-title')
    items = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(episode_img, episode) for episode in episodes]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    results.sort(key= lambda x : x[2], reverse=True)
    print(results)
    # Fetch images in the background
    

def episode_img(episode):
    pattern = r'((\d{2}|\d{1})(nd|st|rd|th) .*? \d{4})'
    date = re.search(pattern, episode.text).group()
    formattedDate = re.sub(r'(\d{1,2})(st|nd|rd|th)', r'\1', date)
    airingDate = parser.parse(formattedDate, dayfirst=True)
    videoLinkSoup = soupObject(episode.find('a')['href'], '.thecontent')
    links = videoLinkSoup.select_one('span:-soup-contains("VKprime")').parent.find_next_sibling('p').select_one('a')['href']
    linkSoup = soupObject(links, '#content')
    iframe = linkSoup.select_one('iframe').get('src')
    imgId = iframe.split("embed-")[1].split(".")[0]
    imgUrl1 = f"https://ovhprime0.vkcdn5.com/i/01/00175/{imgId}.jpg"
    imgUrl2 = f"https://ovhprime111.vkcdn5.com/i/01/00175/{imgId}.jpg"
    if requests.get(imgUrl1).status_code == 200:
        imgis = imgUrl1
        # li.setArt({
        #     'thumb': imgUrl1,
        #     'icon': imgUrl1,
        #     'fanart': imgUrl1
        # })
    elif requests.get(imgUrl2).status_code == 200:
        imgis = imgUrl2
        # li.setArt({
        #     'thumb': imgUrl2,
        #     'icon': imgUrl2,
        #     'fanart': imgUrl2
        # })
    else:
        imgis = "not present"
    
    # Update the list item in Kodi
    return episode.text, imgis, airingDate

episodeList("https://www.yodesitv.info/category/star-plus/ghum-hai-kisikey-pyaar-meiin/")

