import json
import requests

url = "http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp"


def get_game_data():
    nhl_data = requests.get(url)
    nhl_json_data = nhl_data.text[15:-1]
    print(nhl_json_data)
    try:
        output = json.loads(nhl_json_data) #creates dict
    except:
        print('Error processing Json File')
    game_list = output['games']
    for each_game in game_list:
        # print(each_game)
        print(each_game['atn'], each_game['atv'])
        print(each_game['htn'], each_game['htv'])

get_game_data()

