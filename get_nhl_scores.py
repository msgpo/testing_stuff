import json
import requests

url = "http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp"


def get_game_data():
    nhl_data = requests.get(url)
    nhl_json_data = nhl_data.text[15:-1]
    print(nhl_json_data)
    try:
        output = json.loads(nhl_json_data)
    except:
        print('Error processing Json File')
    game_list = output['games']
    print(game_list)

get_game_data()

