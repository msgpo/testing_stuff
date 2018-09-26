import json
import requests
import datetime

url = "http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp"


def get_game_data():
    now = datetime.datetime.now()
    today_string = str(now.month) + '/' + str(now.day)
    date_string = '9/25'
    nhl_data = requests.get(url)
    nhl_json_data = nhl_data.text[15:-1]
    try:
        output = json.loads(nhl_json_data) #creates dict
    except:
        print('Error processing Json File')
    game_list = output['games']
    print(game_list)
    for each_game in game_list:
        game_date = each_game['ts']
        # if "TODAY" in game_date:
        if date_string in game_date:
            # print(each_game[''])
            print(each_game['atn'], each_game['atv'], each_game['ats'], each_game['htn'], each_game['htv'], each_game['hts'])
            # print(each_game['htn'], each_game['htv'], each_game['hts'])

get_game_data()

