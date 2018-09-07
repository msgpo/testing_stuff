import re
import requests


def __testing__(self):
    def __init__():
        self.kodi_ip = "192.168.0.32"
        self.kodi_port = "8080"
        self.kodi_user = ""
        self.kodi_pass = ""
        self.json_header = {'content-type': 'application/json'}
        self.kodi_path = "http://"+self.kodi_user+":"+self.kodi_pass+"@"+self.kodi_ip+":"+self.kodi_port+"/jsonrpc"

    def cv_play():
        cv_payload = '{"jsonrpc": "2.0", "method": "Addons.ExecuteAddon", ' \
                       '"params": { "addonid": "script.cinemavision", "params": ["experience"]},  "id": 1}'
        try:
            cv_response = requests.post(self.kodi_path, data=cv_payload, headers=self.json_header)
            print(cv_response.text)
        except Exception as e:
            print(e)

    def kodi_play():
        play_payload = '{"jsonrpc": "2.0", "method": "player.open", "params": {"item":{"playlistid":1}}}'
        try:
            play_response = requests.post(self.kodi_path, data=play_payload, headers=self.json_header)
            print(play_response.text)
        except Exception as e:
            print(e)

    def list_addons():
        list_payload = '{"jsonrpc": "2.0", "method": "Addons.GetAddons",' \
                       ' "params": {"type": "xbmc.addon.executable"}, "id": "1"}'
        try:
            list_response = requests.post(self.kodi_path, data=list_payload, headers=self.json_header)
            print(list_response.text)
        except Exception as e:
            print(e)



    __init__()
    # kodi_play()
    # cv_play()
    list_addons()

__testing__

