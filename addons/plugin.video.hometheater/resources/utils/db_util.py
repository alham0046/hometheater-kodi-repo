import sqlite3
from resources.lib.soupObj import soupObject
import re
import os


print(os.path.dirname(__file__))


def tvCache(channelList = []):
    # print(channelList)
    path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    conn = sqlite3.connect(os.path.join(path,"tvCache.db"))
    cur = conn.cursor()
    fileCache = """CREATE TABLE IF NOT EXISTS TVshowCache (
                    Channel_Name TEXT,
                    Show_Name TEXT,
                    Show_Poster TEXT,
                    Show_Backdrop TEXT,
                    Show_Url TEXT 
                    Show_Status TEXT)"""
    cur.execute(fileCache)
    conn.commit()
    for chDetail in channelList:
        cur.execute("SELECT * FROM TVshowCache WHERE Show_Name = ?", (chDetail["showname"],))
        if cur.fetchone():
            get_data = cur.execute("SELECT * FROM TVshowCache")
            for i in get_data:
                print(i)
            continue
        cur.execute(""" INSERT INTO TVshowCache (
                    Channel_Name,
                    Show_Name,
                    Show_Poster,
                    Show_Backdrop,
                    Show_Url,
                    Show_Status
                    ) VALUES (?,?,?,?,?,?)""", (chDetail["chname"], chDetail["showname"], chDetail["poster"], chDetail["backdrop"], chDetail["url"], chDetail["Show_Status"]))
        conn.commit()
        print(chDetail["showname"])
    
    conn.close()
def tvEpisodeCache(episodeList = []):
    # print(channelList)
    path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    conn = sqlite3.connect(os.path.join(path,"tvEpisodes.db"))
    cur = conn.cursor()
    fileCache = """CREATE TABLE IF NOT EXISTS tvEpisodes (
                    Channel_Name TEXT,
                    Show_Name TEXT,
                    Episode_Date TEXT,
                    Episode_Title TEXT,
                    Episode_Img TEXT,
                    Episode_Url TEXT)"""
    cur.execute(fileCache)
    conn.commit()
    for epiDetail in episodeList:
        cur.execute("SELECT * FROM tvEpisodes WHERE Show_Name = ?", (epiDetail["title"],))
        if cur.fetchone():
            get_data = cur.execute("SELECT * FROM tvEpisodes")
            for i in get_data:
                print(i)
            continue
        cur.execute(""" INSERT INTO tvEpisodes VALUES (?,?,?,?,?,?)""", (epiDetail["channelname"], epiDetail["showname"], epiDetail["episodedate"] , epiDetail["title"], epiDetail["img"], epiDetail["EpisodeUrl"]))
        conn.commit()
        print(epiDetail["title"])
    
    conn.close()

def updateDatabase(dbname, tablename, updatevar, updatevalue, whereclause, condition):
    path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    conn = sqlite3.connect(os.path.join(path, dbname))
    cur = conn.cursor()
    cur.execute(f"UPDATE {tablename} SET {updatevar} = ? WHERE {whereclause} = ?", (updatevalue, condition))
    conn.commit()
    conn.close()

# def tvshow(url):
#     # url = "https://www.yodesitv.info/star-plus"
#     shows = soupObject(url, '#tab-0-title-1')
#     showLists = shows.find_all('div', attrs={'class': re.compile('^one_')})
#     channelDetail = []
#     for showList in showLists:
#         chdet = {}
#         icon = showList.select_one('div>a>img')['src']
#         fanart = icon.replace('-370x208','') if "-370x208" in icon else icon
#         fileExist = os.path.dirname(__file__)
#         fileimgbd = ("-".join(showList.text.lower().split(" ")) + "_" + "backdrop.webp").replace("---", "").replace(":", "").strip()
#         fileimgposter = ("-".join(showList.text.lower().split(" ")) + "_" + "poster.webp").replace("---", "").replace(":", "").strip()
#         poster = os.path.join(fileExist, "resources", "Images", fileimgposter)
#         backdrop = os.path.join(fileExist, "resources", "Images", fileimgbd)
#         chdet["chname"] = " ".join(url.split("/")[-1].split("-")).upper()
#         chdet["showname"] = showList.text.strip()
#         chdet["poster"] = poster if os.path.exists(poster) else icon
#         chdet["backdrop"] = backdrop if os.path.exists(backdrop) else fanart
#         chdet["url"] = f"https://www.yodesitv.info/category/{'-'.join(chdet['chname'].lower().split(' '))}/{'-'.join(chdet['showname'].lower().split(' '))}/"
#         channelDetail.append(chdet)
#         # print(showList.text)
#     # print(channelDetail)
#     tvCache(channelDetail)
#     return channelDetail

def getdb(dbname, tablename, condition, whereclause, select = "*", orderby = None):
    path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    if os.path.exists(os.path.join(path, dbname)):
        conn = sqlite3.connect(os.path.join(path, dbname))
        cur = conn.cursor()
        if not orderby:
            shows = cur.execute(f"SELECT {select} FROM {tablename} WHERE {whereclause} = ?", (condition,))
        else:
            shows = cur.execute(f"SELECT {select} FROM {tablename} WHERE {whereclause} = ? ORDER BY {orderby}", (condition,))
        return shows.fetchall()
    else:
        return []

        
