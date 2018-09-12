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


# kodi_play()
# cv_play()
# all_addons = list_addons()
# if addon_name in all_addons:
#    print("Found")
#    cv_play()

#else:
#    print("Not Found")
#    kodi_play()

#list_movies()
list_addons()