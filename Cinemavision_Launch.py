import requests
import json
import re

kodi_ip = "192.168.0.32"
kodi_port = "8080"
kodi_user = ""
kodi_pass = ""
json_header = {'content-type': 'application/json'}
kodi_path = "http://"+kodi_user+":"+kodi_pass+"@"+kodi_ip+":"+kodi_port+"/jsonrpc"
addon_name = "script.cinemavision"
#  addon_name = "pmc"


def load_dirty_json(dirty_json):
    regex_replace = [(r"([ \{,:\[])(u)?'([^']+)'", r'\1"\3"'), (r" False([, \}\]])", r' false\1'), (r" True([, \}\]])", r' true\1')]
    for r, s in regex_replace:
        dirty_json = re.sub(r, s, dirty_json)
    clean_json = json.loads(dirty_json)
    return clean_json


def cv_play():
    method = "Addons.ExecuteAddon"
    cv_payload = {
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
        cv_response = requests.post(kodi_path, data=json.dumps(cv_payload), headers=json_header)
        print(cv_response.text)
    except Exception as e:
        print(e)


def PlayMovieById(movieid):
    method = "Player.Open"
    json_params = {
        'jsonrpc': '2.0',
        'method': method,
        'id': 1,
        'params': {
            'item': {
                'movieid': movieid
            }
        }
    }
    print(json_params)


def kodi_play():
    method = "Player.Open"
    play_payload = {
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
        play_response = requests.post(kodi_path, data=json.dumps(play_payload), headers=json_header)
        print(play_response.text)
    except Exception as e:
        print(e)


def list_addons():
    method = "Addons.GetAddons"
    list_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": "1",
        "params": {
            "type": "xbmc.addon.executable"
        }
    }
    try:
        list_response = requests.post(kodi_path, data=json.dumps(list_payload), headers=json_header)
        return list_response.text
    except Exception as e:
        print(e)
        return "NONE"


def list_all_movies():
    method = "VideoLibrary.GetMovies"
    list_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1,
        "params": {
            "properties": [
            ],
        }
    }
    try:
        list_response = requests.post(kodi_path, data=json.dumps(list_payload), headers=json_header)
        the_movies = json.loads(list_response.text)["result"]["movies"]
        return the_movies
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


def show_popup():
    method = "Addons.ExecuteAddon"
    list_payload ={
        "jsonrpc": "2.0",
        "method": method,
        "id": 1,
        "params": {
            "addonid": "script.popup",
            "params": {
                "line1": "Hello World",
                "line2": "Showing this message using",
                "line3": "Combination of Kodi python modules and",
                "line4": "JSON-RPC API interface",
                "line5": "Have fun coding"
            }
        }
    }
    try:
        list_response = requests.post(kodi_path, data=json.dumps(list_payload), headers=json_header)
        return list_response.text
    except Exception as e:
        # print(e)
        return e


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
        # print(e)
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
        # print(e)
        return e


# print(list_all_movies())
print(find_movie_match('spider', list_all_movies()))
# print(list_addons())
# print(show_popup())
# print(clear_playlist())
# print(add_playlist(1))
# print(mute_kodi())
# PlayMovieById(1)
# print(get_movie_id('Arrival', list_all_movies()))
