import sys
import urllib.parse
import xbmc

addon_handle = int(sys.argv[1])

base_url = sys.argv[0]

def build_url(query):
    return base_url + '?' + urllib.parse.urlencode(query)

def log(find, message = "The default value is"):
    xbmc.log(f"{message}: {find}", xbmc.LOGDEBUG)