import json
import requests
import datetime

url = "http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp"


def get_game_data():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)
    print(yesterday, today, tomorrow)
    today_options = "TODAY", "progress", "LIVE"
    nhl_data = requests.get(url)
    nhl_json_data = nhl_data.text[15:-1]
    try:
        output = json.loads(nhl_json_data) #creates dict
    except:
        print('Error processing Json File')
    game_list = output['games']
    game_count = 0
    # print(game_list)
    for each_game in game_list:
        live_options = each_game['ts'], each_game['tsc'], each_game['bs'], each_game['bsc']
        if set(today_options).intersection(live_options):
            print(each_game['atn'], each_game['atv'], each_game['ats'], each_game['htn'], each_game['htv'], each_game['hts'])
            game_count += 1
    print("There are " + str(game_count) +" games today.")

get_game_data()

