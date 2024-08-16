import json
# import xbmc
import requests
import urllib.parse
import time

showCache = {}
cache = {}
TMDB_API_KEY = "bb24eeb9e1135834df4cd07d37ab6fae"
def fetch_tmdb_details(movie_name):
    if movie_name in cache:
        return cache[movie_name]
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={urllib.parse.quote(movie_name)}"
    response = requests.get(search_url)
    if len(response.json()['results']) == 0:
        movie_name = movie_name.split(" ")[0]
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={urllib.parse.quote(movie_name)}"
        response = requests.get(search_url)
    if response.ok:
        data = response.json()
        if data['results']:
            movie = data['results'][0]
            details = {
                'title': movie['title'],
                'release_date': movie['release_date'],
                'poster_path': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie['poster_path'] else "",
                'backdrop_path': f"https://image.tmdb.org/t/p/w1280{movie['backdrop_path']}" if movie['backdrop_path'] else ""
            }
            cache[movie_name] = details
            return details
    return None
def fetch_tmdb_details_webshows(show_name, episode = False):
    if show_name in showCache:
        return showCache[show_name]
    search_url = f"https://api.themoviedb.org/3/search/tv?api_key={TMDB_API_KEY}&query={urllib.parse.quote(show_name)}"
    response = requests.get(search_url)
    if response.ok:
        data = response.json()
        if data['results']:
            showId = data['results'][0]['id']
            showIdUrl = f"https://api.themoviedb.org/3/tv/{showId}?api_key={TMDB_API_KEY}&language=en-US"
            showData = requests.get(showIdUrl)
            showData = showData.json()
            no_of_seasons = showData["number_of_seasons"]
            if episode:
                seasons = []
                for season in showData['seasons']:
                    seasonData = requests.get(f"https://api.themoviedb.org/3/tv/{showId}/season/{season['season_number']}?api_key={TMDB_API_KEY}&language=en-US").json()
                    seasons.append(seasonData)
                details = {
                    'title': showData['name'],
                    'seasons' : seasons,
                    # 'poster_path': f"https://image.tmdb.org/t/p/w500{showData['poster_path']}" if showData['poster_path'] else "",
                    # 'backdrop_path': f"https://image.tmdb.org/t/p/w780{showData['backdrop_path']}" if showData['backdrop_path'] else ""
                }
                showCache[show_name] = details
            else:
                details = {
                    'title': showData['name'],
                    'last_season' : showData["last_episode_to_air"]["season_number"],
                    'last_season_date' : showData["last_air_date"],
                    'poster_path': f"https://image.tmdb.org/t/p/w500{showData['poster_path']}" if showData['poster_path'] else "",
                    'backdrop_path': f"https://image.tmdb.org/t/p/w1280{showData['backdrop_path']}" if showData['backdrop_path'] else ""
                }
            
            
            return details
    return None

# start = time.perf_counter()
# show1 = fetch_tmdb_details_webshows('kota factory', episode=False)
# print(json.dumps(show1, indent=4))
# end = time.perf_counter()
# print(end - start)






# import json
# import xbmc

# def get_tmdb_details(movie_name):
#     # Define the URL for the TMDB Helper plugin
#     tmdb_url = "plugin://plugin.video.themoviedb.helper"
    
#     # Define the JSON-RPC query to get movie details
#     query = {
#         "jsonrpc": "2.0",
#         "method": "Files.GetDirectory",
#         "params": {
#             "directory": f"{tmdb_url}/search/movie?query={movie_name}",
#             "media": "files"
#         },
#         "id": 1
#     }

#     # Send the JSON-RPC request
#     response = xbmc.executeJSONRPC(json.dumps(query))
#     xbmc.log(f"JSON-RPC response: {response}", xbmc.LOGDEBUG)
#     response_data = json.loads(response)
    
#     if 'result' in response_data and 'files' in response_data['result']:
#         for file in response_data['result']['files']:
#             if 'art' in file and 'poster' in file['art']:
#                 return {
#                     'poster_path': file['art']['poster'],
#                 }
#     return None
