import urllib.parse
import xbmc
import sys

def routing(paramstring):
    params = dict(urllib.parse.parse_qsl(paramstring))
    xbmc.log(f"params string is: {paramstring}", xbmc.LOGDEBUG)
    if params:
        if params['mode'] == 'get_channel':
            from resources.lib.tvShowsdir import get_channel
            get_channel()
        elif params['mode'] == "get_movieplatform":
            from resources.lib.movies import get_movieplatform
            get_movieplatform()
        elif params['mode'] == "get_webshowsplatform":
            from resources.lib.webshows import get_webshowsplatform
            get_webshowsplatform()
        elif params['mode'] == 'get_shows':
            from resources.lib.tvShowsdir import get_shows
            get_shows(params['url'])
        elif params['mode'] == 'get_Episodes':
            from resources.lib.tvShowsdir import get_Episodes
            get_Episodes(params['url'])
        elif params['mode'] == 'play_video':
            from resources.lib.tvShowsdir import play_video
            play_video(params['url'])
        elif params['mode'] == 'get_movies':
            from resources.lib.movies import get_moviesList
            get_moviesList(params['url'])
        elif params['mode'] == 'get_webshows':
            from resources.lib.webshows import get_webshowsList
            get_webshowsList(params['url'])
        elif params['mode'] == 'play_movie':
            from resources.lib.movies import play_movie
            play_movie(params['url'])
        elif params['mode'] == 'play_webshow':
            from resources.lib.webshows import play_webshow
            play_webshow(params['url'])
        elif params['mode'] == 'open_webshow':
            from resources.lib.webshows import open_webshow
            open_webshow(params['url'] ,params['seriesName'], params['lastSeason'])
        elif params['mode'] == 'set_status':
            from resources.lib.tvShowsdir import set_status
            set_status(params['showname'], params['status'])
    else:
        from resources.lib.mainMenu import main_menu
        xbmc.log(f"Router params: {params}", xbmc.LOGDEBUG)
        main_menu()

