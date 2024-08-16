import xbmcplugin
import xbmcgui
import sys
import urllib.parse
import xbmc


def build_url(query):
    base_url = sys.argv[0]
    return base_url + '?' + urllib.parse.urlencode(query)

def main_menu():
    addon_handle = int(sys.argv[1])
    url = build_url({'mode': 'get_channel'})
    li = xbmcgui.ListItem('Channels')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    url = build_url({'mode': 'get_movieplatform'})
    li = xbmcgui.ListItem('Movies')
    xbmc.log(f"addon handle is : {addon_handle}", xbmc.LOGDEBUG)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    url = build_url({'mode': 'get_webshowsplatform'})
    li = xbmcgui.ListItem('WebShows')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)