import requests

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
        cv_response = requests.post(kodi_path, data=cv_payload, headers=json_header)
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
        play_response = requests.post(kodi_path, data=play_payload, headers=json_header)
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
        list_response = requests.post(kodi_path, data=list_payload, headers=json_header)
        return list_response.text
    except Exception as e:
        print(e)
        return "NONE"


def list_movies():
    method = "VideoLibrary.GetMovies"
    list_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": "movies",
        "params": {
            "properties": ["year", "premiered", "title"],
            "sort": {
                "order": "ascending", "method": "year"
            }
        }
    }
    try:
        list_response = requests.post(kodi_path, data=list_payload, headers=json_header)
        return list_response.text
    except Exception as e:
        print(e)
        return "NONE"


def show_popup():
    method = "Addons.ExecuteAddon"
    list_payload ={
        "jsonrpc": "2.0",
        "method": method,
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
        list_response = requests.post(kodi_path, data=list_payload, headers=json_header)
        return list_response.text
    except Exception as e:
        # print(e)
        return e


def clear_playlist():
    method = "Playlist.Clear"
    kodi_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": {
            "playlistid": 1
        }
    }
    try:
        kodi_response = requests.post(kodi_path, data=kodi_payload, headers=json_header)
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
        kodi_response = requests.post(kodi_path, data=kodi_payload, headers=json_header)
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
        kodi_response = requests.post(kodi_path, data=kodi_payload, headers=json_header)
        return kodi_response.text
    except Exception as e:
        # print(e)
        return e


# print(list_movies())
# print(list_addons())
# print(show_popup())
# print(clear_playlist())
# print(add_playlist())
# print(mute_kodi())
PlayMovieById(1)
