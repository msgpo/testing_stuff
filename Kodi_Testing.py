import requests
import json
import random

import urllib.error
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import re


kodi_ip = "192.168.0.32"
kodi_port = "8080"
kodi_user = ""
kodi_pass = ""
json_header = {'content-type': 'application/json'}
kodi_path = "http://"+kodi_user+":"+kodi_pass+"@"+kodi_ip+":"+kodi_port+"/jsonrpc"
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
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": "1",
        "params": {
            "type": "xbmc.addon.executable"
        }
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        return kodi_response.text
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
        movie_list = json.loads(kodi_response.text)["result"]["movies"]
        return movie_list
    except Exception as e:
        print(e)
        return "NONE"


def find_movie_match(movie_name, movie_list):
    content = []
    for movie in movie_list:
        movie_title = str(movie['label'])
        if movie_name.lower() in movie_title.lower():
            print(movie['label'])
            info = {
                "label": movie['label'],
                "movieid": movie['movieid']
            }
            content.append(info)
    return content


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


def is_kodi_playing():
    method = "Player.GetActivePlayers"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": "Player.GetActivePlayers",
        "id": 1
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
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
    random_id = random.randint(1,len(full_list))
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


def search_youtube(search_text):
    playlist_results = []
    yt_link = []
    query = urllib.parse.quote(search_text)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    temp_results = re.findall(r'href=\"\/watch\?v=(.{11})', html.decode())
    video_results = list(set(temp_results))
    # print(str(video_results))
    yt_links = soup.find_all("a", class_=" yt-uix-sessionlink spf-link ")
    for each_link in yt_links:
        temp_results = re.findall(r'href=\"\/playlist\?list\=(.*)\"\>View all</a>', each_link.decode())
        if temp_results:
            playlist_results.append(temp_results)
    if playlist_results:
        temp_link = random.choice(playlist_results)
        yt_link = temp_link[0]
    else:
        if "official" in search_text:
            yt_link = video_results[0]
        else:
            temp_link = random.choice(video_results)
            yt_link = temp_link[0]
    print(yt_link)
    print(len(yt_link))
    # return yt_link


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


my_id = search_youtube("captain marvel official trailer")
# print(alt_youtube_search("owl city"))
# print(play_youtube_video(my_id))
# print(alt_youtube_search("captain marvel official trailer"))
# print(push_kodi_notification("this is a test"))
# print(move_cursor("down"))
# print(show_movie_info())
# random_movie_select()
# print(list_all_movies())
# print(find_movie_match('spider', list_all_movies()))
# print(list_addons())
# print(clear_playlist())
# print(add_playlist(1))
# print(mute_kodi())
# play_movie_by_id(50)
# print(get_movie_id('Arrival', list_all_movies()))
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
