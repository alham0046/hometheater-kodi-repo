import sqlite3
from resources.lib.soupObj import soupObject
# from resources.lib.tvShows import get_VideoLink
import re
import os


print(os.path.dirname(__file__))


def tvCache(channelList = []):
    # print(channelList)
    conn = sqlite3.connect("tvCache.db")
    cur = conn.cursor()
    fileCache = """CREATE TABLE IF NOT EXISTS TVshowCache (
                    Channel_Name TEXT,
                    Show_Name TEXT,
                    Show_Poster TEXT,
                    Show_Backdrop TEXT,
                    Show_Url TEXT )"""
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
                    Show_Url
                    ) VALUES (?,?,?,?,?)""", (chDetail["chname"], chDetail["showname"], chDetail["poster"], chDetail["backdrop"], chDetail["url"]))
        conn.commit()
        print(chDetail["showname"])
    
    conn.close()

def tvshow():
    url = "https://www.yodesitv.info/star-bharat/"
    shows = soupObject(url, '#tab-0-title-1')
    showLists = shows.find_all('div', attrs={'class': re.compile('^one_')})
    channelDetail = []
    for showList in showLists:
        chdet = {}
        icon = showList.select_one('div>a>img')['src']
        fanart = icon.replace('-370x208','') if "-370x208" in icon else icon
        fileExist = os.path.dirname(__file__)
        fileimgbd = ("-".join(showList.text.lower().split(" ")) + "_" + "backdrop.webp").replace("---", "").replace(":", "").strip()
        fileimgposter = ("-".join(showList.text.lower().split(" ")) + "_" + "poster.webp").replace("---", "").replace(":", "").strip()
        poster = os.path.join(fileExist, "resources", "Images", fileimgposter)
        backdrop = os.path.join(fileExist, "resources", "Images", fileimgbd)
        chdet["chname"] = " ".join(url.split("/")[-2].split("-")).upper()
        chdet["showname"] = showList.text.strip()
        chdet["poster"] = poster if os.path.exists(poster) else icon
        chdet["backdrop"] = backdrop if os.path.exists(backdrop) else fanart
        chdet["url"] = f"https://www.yodesitv.info/category/{"-".join(chdet['chname'].lower().split(" "))}/{"-".join(chdet['showname'].lower().split(" "))}/"
        channelDetail.append(chdet)
        # print(showList.text)
    # print(channelDetail)
    tvCache(channelDetail)

def getdb(dbname, tablename, whereclause= None, condition = None, select = "*"):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    if condition :
        shows = cur.execute(f"SELECT {select} FROM {tablename} WHERE {whereclause} = ?", (condition,))
    else:
        shows = cur.execute(f"SELECT {select} FROM {tablename}")
    return shows.fetchall()

def deletedb(dbname, tablename, whereclause, condition):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {tablename} WHERE {whereclause} = ?", (condition,))
    conn.commit()
    doclist = getdb(dbname, tablename)
    print(doclist)

# def addColumn(dbname):
#     conn = sqlite3.connect(dbname)
#     cur = conn.cursor()




# tvshow()
# deletedb("tvEpisodes.db", "tvEpisodes", "Channel_Name", "STAR BHARAT")

dblist = getdb(dbname="tvEpisodes.db", tablename="tvEpisodes", whereclause="Channel_Name", condition="STAR BHARAT")
# dblist = getdb(dbname="tvCache.db", tablename="TVshowCache", whereclause="Channel_Name", condition="STAR PLUS", select="Show_Url")
print(dblist)
# value = [val[4] for val in dblist if val[0] == "STAR PLUS"]
# print(value)
        
