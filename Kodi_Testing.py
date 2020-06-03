import requests
import json
import random
import time
import pychromecast
from pychromecast.controllers.youtube import YouTubeController

import urllib.error
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from word2number import w2n


json_header = {'content-type': 'application/json'}
kodi_ip = "192.168.0.32"
kodi_port = "8080"
kodi_user = ""
kodi_pass = ""
kodi_path = "http://"+kodi_user+":"+kodi_pass+"@"+kodi_ip+":"+kodi_port+"/jsonrpc"

hyper_ip = "192.168.0.32"
hyper_port = "19444"
hyper_user = ""
hyper_pass = ""
hyper_path = "http://"+hyper_ip+":"+hyper_port+"/jsonrpc"

addon_name = "script.cinemavision"
#  addon_name = "pmc"


def cv_play():
    method = "Addons.ExecuteAddon"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1,
        "params": {
            "addonid": "script.cinemavision",
            "params": [
                "experience",
                "nodialog"
            ]
        }
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        print(kodi_response.text)
    except Exception as e:
        print(e)


def play_movie_by_id(movieid):
    method = "Player.Open"
    kodi_payload = {
        'jsonrpc': '2.0',
        'method': method,
        'id': 1,
        'params': {
            'item': {
                'movieid': movieid
            }
        }
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        print(kodi_response.text)
    except Exception as e:
        print(e)


def kodi_play():
    method = "Player.Open"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1,
        "params": {
            "item": {
                "playlistid": 1
            }
        }
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        print(kodi_response.text)
    except Exception as e:
        print(e)


def list_addons():
    method = "Addons.GetAddons"
    addon_video = "xbmc.addon.video"
    addon_executable = "xbmc.addon.executable"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": "1",
        "params": {
            "type": addon_video
        }
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        return kodi_response.text
    except Exception as e:
        print(e)
        return "NONE"


def check_youtube_addon():
    method = "Addons.GetAddons"
    addon_video = "xbmc.addon.video"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": "1",
        "params": {
            "type": addon_video
        }
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
    except Exception as e:
        print(e)
        return False
    if "plugin.video.youtube" in kodi_response.text:
        return True
    else:
        return False


def check_cinemavision_addon():
    method = "Addons.GetAddons"
    addon_video = "xbmc.addon.executable"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": "1",
        "params": {
            "type": addon_video
        }
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
    except Exception as e:
        print(e)
        return False
    if "script.cinemavision" in kodi_response.text:
        return True
    else:
        return False


def find_movie_with_filter(movie_name=""):
    print('Searching for: ' + movie_name)
    temp_list = []
    method = "VideoLibrary.GetMovies"
    if movie_name == '':
        kodi_payload = {
            "jsonrpc": "2.0",
            "method": method,
            "id": 1,
            "params": {
                "properties": [
                ],
            }
        }
    else:
        kodi_payload = {
            "jsonrpc": "2.0",
            "params": {
                "sort": {
                    "order": "ascending",
                    "method": "title"},
                "filter": {
                    "operator": "contains",
                    "field": "title",
                    "value": movie_name
                },
                "properties": [
                ]
            },
            "method": method,
            "id": 1
        }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        movie_list = json.loads(kodi_response.text)["result"]["movies"]
        print(movie_list)
        for each_movie in movie_list:
            movie_title = str(each_movie['label'])
            info = {
                "label": each_movie['label'],
                "movieid": each_movie['movieid']
            }
            if movie_title not in str(temp_list):
                temp_list.append(info)
            else:
                if len(each_movie['label']) == len(movie_title):
                    print('found duplicate')
                else:
                    temp_list.append(info)
        movie_list = temp_list
        return movie_list
    except Exception as e:
        print(e)
        return "NONE"


def get_sources():
    method = "Files.GetSources"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1,
        "params": {
            "media": "video"
        }
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        print(kodi_response.text)
        movie_list = json.loads(kodi_response.text)["result"]["movies"]
        # print(json.loads(kodi_response.text)["result"]["limits"]["total"])
        return movie_list
    except Exception as e:
        print(e)
        return "NONE"


def list_all_movies():
    method = "VideoLibrary.GetMovies"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1,
        "params": {
            "properties": [
            ],
        }
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        print(kodi_response.text)
        movie_list = json.loads(kodi_response.text)["result"]["movies"]
        # print(json.loads(kodi_response.text)["result"]["limits"]["total"])
        return movie_list
    except Exception as e:
        print(e)
        return "NONE"

def list_filtered_movies(searchItem):
    method = "VideoLibrary.GetMovies"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1,
        "params": {
            "properties": [
            ],
            "filter": {
                "field": 'title',
                "operator": "contains",
                "value": searchItem
            },

        }
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        print(kodi_response.text)
        movie_list = json.loads(kodi_response.text)["result"]["movies"]
        # print(json.loads(kodi_response.text)["result"]["limits"]["total"])
        return movie_list
    except Exception as e:
        print(e)
        return "NONE"




def begin_cast(mylink):
    cast = pychromecast.Chromecast('192.168.0.37')
    cast.wait()
    mc = cast.media_controller
    print(mylink)
    mc.play_media(mylink, 'video/mp4')
    # mc.play_media('rtsp://192.168.0.22:8554/', 'video/mp4')
    time.sleep(7)
    mc.block_until_active()
    mc.play()
    mc.stop()


def get_movie_path(movieID):
    method = "VideoLibrary.GetMovieDetails"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1,
        "params": {"movieid": movieID,
                   "properties": [
                       #"art",
                       #"cast",
                       #"dateadded",
                       #"director",
                       #"fanart",
                       "file",
                       #"genre",
                       #"imdbnumber",
                       #"lastplayed",
                       #"mpaa",
                       #"originaltitle",
                       #"playcount",
                       #"plot",
                       #"plotoutline",
                       #"premiered",
                       #"rating",
                       #"runtime",
                       #"resume",
                       #"setid",
                       #"sorttitle",
                       #"streamdetails",
                       #"studio",
                       #"tagline",
                       #"thumbnail",
                       #"title",
                       #"trailer",
                       #"userrating",
                       #"votes",
                       #"writer"
                   ],
                   }
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        movie_path = json.loads(kodi_response.text)["result"]["moviedetails"]["file"]
        basePath = 'http://'+kodi_ip+':'+kodi_port+'/vfs/'
        url_path = basePath + urllib.parse.quote(movie_path, safe='')
        print(url_path)
        return url_path
    except Exception as e:
        print(e)
        return "NONE"


def find_movie_match(movie_name, movie_list):
    content = []  # this is a dict
    for movie in movie_list:
        movie_title = str(movie['label']).lower()
        if movie_name.lower() in movie_title.lower():
            # print(movie['label'])
            info = {
                "label": movie['label'],
                "movieid": movie['movieid']
            }
            print('current movie: ' + movie['label'])
            # print(content)
            for entry in content:
                print(entry['label'])
            content.append(info)
            print(content)
    return content


def search_move(title):
    title = numeric_replace(title)
    foundList = []  # this is a dict
    movieList = list_all_movies()
    titleList = title.replace("-", "").lower().split()
    ## check each movie in the list for strings that match all the words in the search
    for each_movie in movieList:
        movieName = each_movie["label"].replace("-", "")
        moveName = numeric_replace(movieName)
        if all(words in movieName.lower() for words in titleList):
            print("Found " + movieName + " : " + "MovieID: " + str(each_movie["movieid"]))
            info = {
                "label": each_movie['label'],
                "movieid": each_movie['movieid']
            }
            foundList.append(info)
    ## remove duplicates
    temp_list = []  # this is a dict
    for each_movie in foundList:
        movie_title = str(each_movie['label'])
        info = {
            "label": each_movie['label'],
            "movieid": each_movie['movieid']
        }
        if movie_title not in str(temp_list):
            temp_list.append(info)
        else:
            if len(each_movie['label']) == len(movie_title):
                print('found duplicate')
            else:
                temp_list.append(info)
    foundList = temp_list
    return foundList  # returns a dictionary of matched movies

def search_music_item(search_item, exact_match=False, filter="label"):
    #filter options: label, artist, album
    #print(exact_match)
    search_item = numeric_replace(search_item)
    foundList = []  # this is a dict
    musicList = list_all_music()
    search_words = search_item.replace("-", "").lower().split()
    search_length = len(search_words)
    ## check each movie in the list for strings that match all the words in the search
    for each_song in musicList:
        #print(str(each_song))
        if filter == "artist":
            itemName = each_song[filter][0].replace("-", "")
        else:
            print("not filtered by artist: " + str(each_song))
            itemName = each_song[filter].replace("-", "")
        if len(itemName) > 0:
            #print(itemName.lower())
            itemName = numeric_replace(itemName)
            if all(words in itemName.lower() for words in search_words):
                found_length = len(each_song['label'].split())
                if exact_match:
                    if found_length == search_length:
                        #print("Found Item: " + itemName + " : " + "SongID: " + str(each_song["songid"]))
                        info = {
                            "label": each_song['label'],
                            "songid": each_song['songid'],
                            "artist": each_song['artist']
                        }
                        foundList.append(info)
                else:
                    #print("Found Item: " + itemName + " : " + "SongID: " + str(each_song["songid"]))
                    info = {
                        "label": each_song['label'],
                        "songid": each_song['songid'],
                        "artist": each_song['artist']
                    }
                    foundList.append(info)
    ## remove duplicates
    temp_list = []  # this is a dict
    for each_song in foundList:
        song_title = str(each_song['label'])
        info = {
            "label": each_song['label'],
            "songid": each_song['songid'],
            "artist": each_song['artist']
        }
        if song_title not in str(temp_list):
            temp_list.append(info)
        else:
            if len(each_song['label']) == len(song_title):
                print('found duplicate')
            else:
                temp_list.append(info)
    foundList = temp_list
    #print(str(foundList))
    return foundList  # returns a dictionary of matched movies


def fuzzy_search(title):
    foundList = []  # this is a dict
    movieList = list_all_movies()
    foundList = process.extract(title, movieList)
    print(len(foundList))
    return foundList  # returns a dictionary of matched movies


def numeric_replace(in_words=""):
    word_list = in_words.split()
    return_list = []
    for each_word in word_list:
        try:
            new_word = w2n.word_to_num(each_word)
        except Exception as e:
            #print(e)
            new_word = each_word
        return_list.append(new_word)
        return_string = ' '.join(str(e) for e in return_list)
    return return_string




def get_movie_id(movie_name, movie_list):
    movie_id = 'NONE'
    for movie in movie_list:
        if movie_name == movie['label']:
            movie_id = movie['movieid']
    return movie_id



def clear_playlist():
    method = "Playlist.Clear"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1,
        "params": {
            "playlistid": 1
        }
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        return kodi_response.text
    except Exception as e:
        return e


def add_playlist(movieid):
    method = "Playlist.Add"
    kodi_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": {
            "playlistid": 1,
            "item": {
                "movieid": movieid
            }
        }
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        return kodi_response.text
    except Exception as e:
        # print(e)
        return e


def mute_kodi():
    method = "Application.SetMute"
    kodi_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": {
            "mute": "toggle"
        }
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        return kodi_response.text
    except Exception as e:
        return e

def update_library():
    method = "VideoLibrary.Scan"
    kodi_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": {
            "showdialogs": True
        }
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        return kodi_response.text
    except Exception as e:
        return e


def clean_library():
    method = "VideoLibrary.Clean"
    kodi_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": {
            "showdialogs": True
        }
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        return kodi_response.text
    except Exception as e:
        return e


def reboot_kodi():
    method = "System.Reboot"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        return kodi_response.text
    except Exception as e:
        return e


def shutdown_kodi():
    method = "System.Shutdown"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        return kodi_response.text
    except Exception as e:
        return e

def kodi_send_text(text):
    method = "Input.SendText"
    kodi_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": {
            "text": text
        }
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        return kodi_response.text
    except Exception as e:
        return e


def skip_fwd():
    method = "Player.Seek"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": {
            "playerid": 1,
            "value": "smallforward"
        },
        "id": 1
    }
    if is_kodi_playing():
        try:
            kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
            return kodi_response.text
        except Exception as e:
            return e


def skip_rev():
    method = "Player.Seek"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": {
            "playerid": 1,
            "value": "smallbackward"
        },
        "id": 1
    }
    if is_kodi_playing():
        try:
            kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
            return kodi_response.text
        except Exception as e:
            return e


# {"jsonrpc":"2.0","method":"Application.SetVolume","params":{"volume":100},"id":1}
def set_volume(level):
    method = "Application.SetVolume"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": {
            "volume": level
        },
        "id": 1
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        # print(json.loads(kodi_response.text)["result"])
        return json.loads(kodi_response.text)["result"]
    except Exception as e:
        return e

def pause_movie():
    method = "Player.PlayPause"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": {
            "playerid": 1,
            "play": False},
        "id": 1
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        return kodi_response.text
    except Exception as e:
        return e


def resume_movie():
    method = "Player.PlayPause"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": {
            "playerid": 1,
            "play": True},
        "id": 1
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        return kodi_response.text
    except Exception as e:
        return e


def stop_movie():
    method = "Player.Stop"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": {
            "playerid": 1
        },
        "id": 1
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        return kodi_response.text
    except Exception as e:
        return e


def subtitles_on():
    method = "Player.SetSubtitle"
    kodi_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": {
            "playerid": 1,
            "subtitle": "on"
        }
    }
    if is_kodi_playing():
        try:
            kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
            return kodi_response.text
        except Exception as e:
            return e
    else:
        return "kodi not playing"


def subtitles_off():
    method = "Player.SetSubtitle"
    kodi_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": {
            "playerid": 1,
            "subtitle": "off"
        }
    }
    if is_kodi_playing():
        try:
            kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
            return kodi_response.text
        except Exception as e:
            return e
    else:
        return "Kodi not playing"


def show_movies_added():
    method = "GUI.ActivateWindow"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": {
            "window": "videos",
            "parameters": [
                "videodb://recentlyaddedmovies/"
            ]
        },
        "id": "1"
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        print(kodi_response.text)
        return kodi_response.text
    except Exception as e:
        return e


def show_movies_genre():
    method = "GUI.ActivateWindow"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": {
            "window": "videos",
            "parameters": [
                "videodb://movies/genres/"
            ]
        },
        "id": "1"
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        print(kodi_response.text)
        return kodi_response.text
    except Exception as e:
        return e


def show_movies_actors():
    method = "GUI.ActivateWindow"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": {
            "window": "videos",
            "parameters": [
                "videodb://movies/actors/"
            ]
        },
        "id": "1"
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        print(kodi_response.text)
        return kodi_response.text
    except Exception as e:
        return e


def show_movies_studios():
    method = "GUI.ActivateWindow"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": {
            "window": "videos",
            "parameters": [
                "videodb://movies/studios/"
            ]
        },
        "id": "1"
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        print(kodi_response.text)
        return kodi_response.text
    except Exception as e:
        return e


def show_movies_title():
    method = "GUI.ActivateWindow"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": {
            "window": "videos",
            "parameters": [
                "videodb://movies/titles/"
            ]
        },
        "id": "1"
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        print(kodi_response.text)
        return kodi_response.text
    except Exception as e:
        return e


def show_movies_sets():
    method = "GUI.ActivateWindow"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": {
            "window": "videos",
            "parameters": [
                "videodb://movies/sets/"
            ]
        },
        "id": "1"
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        print(kodi_response.text)
        return kodi_response.text
    except Exception as e:
        return e


def show_root():
    method = "GUI.ActivateWindow"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": {
            "window": "videos",
            "parameters": [
                "library://video/"
            ]
        },
        "id": "1"
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        print(kodi_response.text)
        return kodi_response.text
    except Exception as e:
        return e


def show_movies():
    show_root()
    method = "GUI.ActivateWindow"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": {
            "window": "videos",
            "parameters": [
                "videodb://movies/"
            ]
        },
        "id": "1"
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        print(kodi_response.text)
        return kodi_response.text
    except Exception as e:
        return e


def is_kodi_playing():  #
    method = "Player.GetActivePlayers"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": "Player.GetActivePlayers",
        "id": 1
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        print(kodi_response.text)
        # {"id":1,"jsonrpc":"2.0","result":[{"playerid":1,"playertype":"internal","type":"video"}]}
        #
        parse_response = json.loads(kodi_response.text)["result"]
        if not parse_response:
            playing_status = False
        else:
            playing_status = True
        print("Kodi Playing Status:", playing_status)
        return playing_status
    except Exception as e:
        return e



def random_movie_select():
    full_list = list_all_movies()
    random_id = random.randint(1, len(full_list))
    selected_entry = full_list[random_id]
    selected_name = selected_entry['label']
    selected_id = selected_entry['movieid']
    print(selected_name, selected_id)

def show_movie_info():
    method = "Input.Info"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        return kodi_response.text
    except Exception as e:
        return e



def move_cursor(dir):
    method = "Input." +dir.capitalize()
    print(method)
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        return kodi_response.text
    except Exception as e:
        return e

def push_kodi_notification(message):
    method = "GUI.ShowNotification"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": {
            "title": "uTorrent",
            "message": message
        },
        "id": 1
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        return kodi_response.text
    except Exception as e:
        return e


def get_youtube_links(search_list):
    print(search_list)
    search_text = str(search_list)
    print(search_text)
    query = urllib.parse.quote(search_text)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    # Get all video links from page
    temp_links = []
    all_video_links = re.findall(r'href=\"\/watch\?v=(.{11})', html.decode())
    for each_video in all_video_links:
        print(each_video)
        if each_video not in temp_links:
            temp_links.append(each_video)
    video_links = temp_links
    # Get all playlist links from page
    temp_links = []
    all_playlist_results = re.findall(r'href=\"\/playlist\?list\=(.{34})', html.decode())
    sep = '"'
    for each_playlist in all_playlist_results:
        if each_playlist not in temp_links:
            cleaned_pl = each_playlist.split(sep, 1)[0]
            temp_links.append(cleaned_pl)
    playlist_links = temp_links
    yt_links = []
    if video_links:
        yt_links.append(video_links[0])
    if playlist_links:
        yt_links.append(playlist_links[0])
    # print(yt_links)
    # print(len(yt_links))
    return yt_links


def play_youtube_video(video_id):
    method = "Player.Open"
    # Playlist links are 34 characters long
    # individual links are 11 characters long
    if len(video_id) > 30:
        yt_link = "plugin://plugin.video.youtube/play/?playlist_id=" + video_id + "&play=1&order=shuffle"
    else:
        yt_link = "plugin://plugin.video.youtube/play/?video_id=" + video_id
    kodi_payload = {
        "jsonrpc": "2.0",
        "params": {
            "item": {
                "file": yt_link
            }
        },
        "method": method,
        "id": "libPlayer"
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        if "OK" in kodi_response:
            show_context_menu()
        return kodi_response.text
    except Exception as e:
        return e

def stop_youtube():
    method = "Player.Stop"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": {
            "playerid": 1
        },
        "id": "libPlayer"
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        if "OK" in kodi_response:
            show_context_menu()
        return kodi_response.text
    except Exception as e:
        return e


def show_context_menu():
    method = "Input.ContextMenu"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        return kodi_response.text
    except Exception as e:
        return e

def youtube_query_regex(req_string):
    return_list = []
    pri_regex = re.search(r'play (?P<item1>.*) from youtube', req_string)
    sec_regex = re.search(r'play some (?P<item1>.*) from youtube|play the (?P<item2>.*)from youtube', req_string)
    if pri_regex:
        if sec_regex:  # more items requested
            # multiple = True
            temp_results = sec_regex
        else:  # single item requested
            # multiple = False
            temp_results = pri_regex
    if temp_results:
        item_result = temp_results.group(temp_results.lastgroup)
        return_list = item_result
        # print(return_list)
        return return_list


def connect_to_websocket():
    hyper_payload = {
        "color": [255, 255, 255],
        "command": "color",
        "priority": 100
    }
    try:
        hyper_response = requests.put(hyper_path, data=json.dumps(hyper_payload), headers=json_header)
        print(hyper_response.text)
    except Exception as e:
        print(e)

def location_regex(message):
    return_list = []
    regex_string = r".*((to the|to)|(at the|at)) (?P<location>.*)"
    message_split = message.split(" ")
    print(message_split)
    pri_regex = re.search(regex_string, message)
    if pri_regex:
        ret_location = pri_regex.group("location")
        #print(ret_location)
        return ret_location

def test_string(mystring):
    if mystring[-1] == "/":
        mystring = mystring[0:-1]
    if mystring[0] == "/":
        mystring = mystring[1:]
    print(mystring)

def list_all_music():
    method = "AudioLibrary.GetSongs"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1,
        "params": {
            "properties": [
                "artist",
                "duration",
                "album",
                "track"
            ],
        }
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        #print(kodi_response.text)
        song_list = json.loads(kodi_response.text)["result"]["songs"]
        #print(json.loads(kodi_response.text)["result"]["songs"])
        return song_list
    except Exception as e:
        print(e)
        return "NONE"

def filter_music(searchItem, filterType):
    method = "AudioLibrary.GetSongs"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1,
        "params": {
            "properties": [
                "artist",
                "duration",
                "album",
                "track"
            ],
            "filter": {
                "field": filterType,
                "operator": "contains",
                "value": searchItem
            },
            "sort": {
                "order": "ascending",
                "method": "track",
                "ignorearticle": True
            }
        }
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        #print(kodi_response.text)
        song_list = json.loads(kodi_response.text)["result"]["songs"]
        #print(json.loads(kodi_response.text)["result"]["songs"])
        return song_list
    except Exception as e:
        print(e)
        return "NONE"




def add_song_playlist(songid):
    method = "Playlist.Add"
    kodi_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": {
            "playlistid": 1,
            "item": {
                "songid": songid
            }
        }
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        return kodi_response.text
    except Exception as e:
        # print(e)
        return e

def search_music_library(search_string, category="any"):
    foundList = []  # this is a dict
    if category == "any":
        foundList = search_music_item(search_string, filter="label")
        if len(foundList) > 0:
            return foundList
        print("Label: " + search_string + ", Not Found!")
        foundList = search_music_item(search_string, filter="artist")
        if len(foundList) > 0:
            return foundList
        print("Artist: " + search_string + ", Not Found!")
        foundList = search_music_item(search_string, filter="album")
        if len(foundList) == 0:
            print("Album: " + search_string + ", Not Found!")
            return
    else:
        foundList = search_music_item(search_string, filter=str(category))
    if len(foundList) > 0:
        return foundList

def queue_and_play_music(musicList):
    clear_playlist()
    for each_song in musicList:
        print(each_song["label"], each_song["songid"])
        add_song_playlist(each_song["songid"])
        kodi_play()


def parse_music_utterance(message):
    return_type = "any"
    primary_regex = r"((?<=album) (?P<album>.*$))|((?<=artist) (?P<artist>.*$))|((?<=song) (?P<label>.*$))"
    print(message)
    if (message.find('some') != -1):
        secondary_regex = r"((?<=some) (?P<any>.*$))"
    else:
        secondary_regex = r"((?<=play) (?P<any>.*$))"
    key_found = re.search(primary_regex, message)
    if key_found:
        if key_found.group("label"):
            print("found label")
            return_item = key_found.group("label")
            return_type = "label"
        elif key_found.group("artist"):
            print("found artist")
            return_item = key_found.group("artist")
            return_type = "artist"
        elif key_found.group("album"):
            print("found album")
            return_item = key_found.group("album")
            return_type = "album"
    else:
        key_found = re.search(secondary_regex, message)
        if key_found.group("any"):
            return_item = key_found.group("any")
            return_type = "any"
    return return_item, return_type


#play_this = parse_music_utterance("ask kodi to play the song speak life")
#get_music = search_music_library(play_this[0], category=play_this[1])
#print(get_music)
#print(filter_music)
#musicLibrary = list_all_music()
#musicLibrary = filter_music('styx', 'artist')
#musicLibrary = filter_music('hits', 'album')
#musicLibrary = filter_music('speak life', 'title')
#print(str(musicLibrary))
#queue_and_play_music(get_music)

#print(get_music)
#print(parse_music_utterance("ask kodi to play all shook up"))
#print(parse_music_utterance("ask kodi to play the album appeal to reason"))
#print(parse_music_utterance("ask kodi to play elvis Presley"))

#myMusic = list_all_music()
#print(myMusic)
#print(search_music_label('Styx', filter="artist"))
#print(search_music_artist('Styx'))
#get_music = search_music_library('Greatest Hits')
#print(search_music_library('Greatest Hits'))
#print(str(get_music))
#queue_and_play_music(get_music)

#for each_album in list_all_music():
#    print(each_album)
#    print(each_album["label"])
#    print(each_album["artist"][0])

#add_song_to_playlist(266)
#kodi_play()

#stop_movie()

# print(set_volume(75))
# print(connect_to_websocket())
# my_search = youtube_query_regex("play third day from youtube")
# print(my_search)
# my_id = get_youtube_links(my_search)
# print(my_id)
# print(len(my_id))
# print(play_youtube_video(my_id))
# print(stop_youtube())
# print(alt_youtube_search("owl city"))
# print(alt_youtube_search("captain marvel official trailer"))
# print(push_kodi_notification("this is a test"))
# print(move_cursor("down"))
# print(show_movie_info())
# random_movie_select()
# print(list_all_movies())
# print(get_movie_id(find_movie_match('spider', list_all_movies()),list_all_movies()))
# print(find_movie_match('spider', list_all_movies()))
# print(find_movie_with_filter('spider'))
# print(check_youtube_addon())
# print(check_cinemavision_addon())
# print(clear_playlist())
# print(add_playlist(1))
# print(mute_kodi())
# play_movie_by_id(50)
# print(get_movie_id('spider man', list_all_movies()))
#movielist = list_all_movies()
movielist = list_filtered_movies('spider')
print(movielist)
#mySearch = "ant man"
#myList = search(mySearch)
#myID = myList[0]["movieid"]
#fileName = get_details(myID)
#begin_cast(fileName)
# print(numeric_replace(mySearch))
# print(mySearch)
#print(search(mySearch))

#get_details()
# get_sources()
#print(fuzzy_search(mySearch))
# print(json.loads(str(movielist))["movies"])
# update_library()
# clean_library()
# reboot_kodi()
# print(subtitles_on())
# print(subtitles_off())
# print(show_movies_added())
# print(show_movies_genre())
# print(show_movies_actors())
# print(show_movies_studios())
# print(show_movies_title())
# print(show_movies_sets())
# print(show_movies())
# print(skip_fwd())
# print(skip_rev())
# print(stop_movie())
# print(is_kodi_playing())
# movie_list = find_movie_with_filter('spider-man')
# print(movie_list)
# print("possible movies are: " + movie_list)
