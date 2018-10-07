import json
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from time import sleep
import datetime

url = "http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp"


def get_game_data():
    # today_options = "TODAY", "progress", "LIVE"
    today_options = "final", "FINAL"
    todays_games = []
    nhl_data = requests.get(url)
    nhl_json_data = nhl_data.text[15:-1]
    try:
        output = json.loads(nhl_json_data) #creates dict
    except:
        print('Error processing Json File')
    game_list = output['games']
    game_count = 0
    for each_game in game_list:
        print(each_game)
        live_options = each_game['ts'], each_game['tsc'], each_game['bs'], each_game['bsc']
        if set(today_options).intersection(live_options):
            if each_game['ats'] > each_game['hts']:
                todays_games.append([each_game['atn'], each_game['ats'], each_game['htn'], each_game['hts']])
            else:
                todays_games.append([each_game['htn'], each_game['hts'], each_game['atn'], each_game['ats']])
            game_count += 1
    return todays_games

print(get_game_data())

