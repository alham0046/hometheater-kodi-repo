from bs4 import BeautifulSoup
import requests
from datetime import datetime
import time
import re
# import re
# from resources.lib.soupObj import soupObject
# from datetime import datetime
# from dateutil import parser
# from resources.lib.soupObj import soupObject

# show_data = {
#     1: [{'title': 'Episode 1'}, {'title': 'Episode 2'}],
#     2: [{'title': 'Episode 1'}, {'title': 'Episode 2'}],
#     3: [{'title': 'Episode 1'}, {'title': 'Episode 2'}]
# }

# print(show_data)
# for season, episode in show_data.items():
#     print(episode[0]["title"])

# a = {}
# a['url'] = {'a' : "google.com"}
# a['url1'] = {'a' : "google1.com"}
# a['url2'] = {'a' : "google2.com"}
# for i,j in a.items():
#     print(i, j['a'])

# a = ['alham', 'faishal', 'vipul']
# for i,j in enumerate(a):
#     print(i, j)

# {
#     '1': [{'Episode 1': 'https:xyz.mkv'}],
#     '3': [{'Episode 2': 'https:xyz2.mkv'}, {'Episode 1': 'https:xyz3.mkv'}],
#     '2': [{'Episode 5': 'https://abc.mkv'}, {'Episode 3': 'https://def.mkv'}]
# }

html = """
<div class="entry-content">
    <h5 style="text-align: center;"><strong><span style="color:#fff;">Season 5 Netflix <span style="color: #FFA500;">[Hindi DD5.1]</span> 720p WEB-DL x264 [400MB/E]</span> </strong></h5>
    <hr>
    <h5 style="text-align: center;"><strong><span style="color:#fff;">Season 3 Netflix <span style="color: #FFA500;">[Hindi DD5.1]</span> 720p WEB-DL x264 [400MB/E]</span> </strong></h5>
    <p style="text-align: center;"><a href="https://example.com/season3/720p" rel="nofollow noopener noreferrer" target="_blank"><button class="dwd-button">Download Now</button></a></p>
    <h5 style="text-align: center;"><strong><span style="color:#fff;">Season 3 Netflix <span style="color: #FFA500;">[Hindi DD5.1]</span> 1080p WEB-DL x264 [1GB/E]</span> </strong></h5>
    <p style="text-align: center;"><a href="https://example.com/season3/1080p" rel="nofollow noopener noreferrer" target="_blank"><button class="dwd-button">Download Now</button></a></p>
</div>
"""
# soup = BeautifulSoup(html, 'html.parser')
# hrtags = soup.hr.find_next_siblings()
# reqtag = next(x for x in hrtags if "1080" in x.text)
# print(reqtag)

# url = "https://gamerxyt.com/hubcloud.php?host=vcloud&id=qus12krjb0vjbj8&token=TWRjekV4bmtCemxDcys5Yk4wNGNqWTZCeXdLMktHb2xQS2lUSFczUGtSMD0="
# req = requests.get(url)
# soup = BeautifulSoup(req.content, 'html.parser')
# mp4Url = soup.select_one('a[href*="pixeldra"]')['href']
# print(mp4Url)

# a = "Ghum Hai Kisikey Pyaar Meiin 1st August 2024 Video Episode Update Online"
# b = r'((\d{2}|\d{1})(nd|st|rd|th) .*? \d{4})'
# c = re.search(b, a).group()
# d = re.sub(r'(\d{1,2})(st|nd|rd|th)', r'\1', c)
# dateformat = "%d %B %Y"
# print(parser.parse(d, dayfirst=True))

# from datetime import datetime

# def get_ordinal(n):
#     start = time.perf_counter()
#     if n.endswith("1"):
#         e = "st"
#     elif n.endswith("2"):
#         e = "nd"
#     elif n.endswith("3"):
#         e = "rd"
#     else:
#         e = "th"
#     print(n+e)
#     end = time.perf_counter()
#     print(end - start)
#     # return "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])
#     return n+e

# # Get today's date
# # today = datetime.today()
# today = datetime(2024, 5, 23)

# # Format the date
# formatted_date = f"{get_ordinal(str(today.day))} {today.strftime('%B')} {today.year}"

# # Print the formatted date
# print(f"Formatted date: {formatted_date}")

url = "https://hls.tvlogy.to/cdn/hls/5a4cca12f470b4e3a871a33e7c876d09/master.txt"
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')
print(soup.prettify)

