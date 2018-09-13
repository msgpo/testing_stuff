import requests
import time


kodi_ip = "192.168.0.32"
kodi_port = "8080"
kodi_user = ""
kodi_pass = ""
json_header = {'content-type': 'application/json'}
kodi_path = "http://"+kodi_user+":"+kodi_pass+"@"+kodi_ip+":"+kodi_port+"/jsonrpc"
addon_name = "script.cinemavision"
#  addon_name = "pmc"

def cv_play():
    cv_payload = '{"jsonrpc": "2.0", "method": "Addons.ExecuteAddon", ' \
                       '"params": { "addonid": "script.cinemavision", "params": ["experience", "nodialog"]},  "id": 1}'
    try:
        cv_response = requests.post(kodi_path, data=cv_payload, headers=json_header)
        print(cv_response.text)
    except Exception as e:
        print(e)

def kodi_play():
    play_payload = '{"jsonrpc": "2.0", "method": "player.open", "params": {"item":{"playlistid":1}}, "id": 1}'
    try:
        play_response = requests.post(kodi_path, data=play_payload, headers=json_header)
        print(play_response.text)
    except Exception as e:
        print(e)

def list_addons():
    list_payload = '{"jsonrpc": "2.0", "method": "Addons.GetAddons",' \
                       ' "params": {"type": "xbmc.addon.executable"}, "id": "1"}'
    try:
        list_response = requests.post(kodi_path, data=list_payload, headers=json_header)
        return list_response.text
    except Exception as e:
        print(e)
        return "NONE"

def list_movies():
    list_payload = '{ "jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", ' \
                   '"params": { "properties": ["year", "premiered", "title"], ' \
                   '"sort": { "order": "ascending", "method": "year" } }, "id": "movies" }'
    try:
        list_response = requests.post(kodi_path, data=list_payload, headers=json_header)
        return list_response.text
    except Exception as e:
        print(e)
        return "NONE"

def show_popup():
    list_payload ='{"jsonrpc": "2.0", "method": "Addons.ExecuteAddon", ' \
                  '"params": {"addonid": "script.popup", "params": {"line1": "Hello World", ' \
                  '"line2": "Showing this message using", "line3": "Combination of Kodi python modules and", ' \
                  '"line4": "JSON-RPC API interface", "line5": "Have fun coding"}}}'
    try:
        list_response = requests.post(kodi_path, data=list_payload, headers=json_header)
        return list_response.text
    except Exception as e:
        # print(e)
        return e


def clear_playlist():
    kodi_payload = '{"jsonrpc":"2.0","id":1,"method":"Playlist.Clear","params":{"playlistid":1}}'
    try:
        kodi_response = requests.post(kodi_path, data=kodi_payload, headers=json_header)
        return kodi_response.text
    except Exception as e:
        # print(e)
        return e

def add_playlist():
    kodi_payload = '{"jsonrpc":"2.0","id":1,"method":"Playlist.Add","params":{"playlistid":1,' \
                   '"item":{"file":"Media/Big_Buck_Bunny_1080p.mov"}}}'
    try:
        kodi_response = requests.post(kodi_path, data=kodi_payload, headers=json_header)
        return kodi_response.text
    except Exception as e:
        # print(e)
        return e

def mute_kodi():
    kodi_payload = '{"jsonrpc": "2.0", "id": 1, "method": "Application.SetMute", "params": {"mute":"toggle"}}'
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
print(mute_kodi())