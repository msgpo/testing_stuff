import json
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from time import sleep
import datetime

url = "http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp"
my_team = []

def get_game_data():
    today_options = "TODAY", "progress", "LIVE"
    complete_options = "final", "FINAL"
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
        #print(each_game)
        live_options = each_game['ts'], each_game['tsc'], each_game['bs'], each_game['bsc']
        print(live_options)
        if set(today_options).intersection(live_options):
            if each_game['ats'] > each_game['hts']:
                todays_games.append([each_game['atn'], each_game['ats'], each_game['htn'], each_game['hts']])
            else:
                todays_games.append([each_game['htn'], each_game['hts'], each_game['atn'], each_game['ats']])
            game_count += 1
    return todays_games


def get_score_response(team_name):
    game_list = get_game_data()
    for each_game in game_list:
        # print(each_game)
        if team_name in str(each_game):
            team_index = each_game.index(team_name)
            team_score = (each_game[team_index + 1])
            print(each_game)
            if team_index > 1:
                other_team = each_game[0]
                other_score = each_game[1]
            else:
                other_team = each_game[2]
                other_score = each_game[3]
            response = "The current score is, " + str(team_name) + ", " + team_score
            break
        else:
            response = "There are no games today that include, " + str(team_name)


    return response

print(get_score_response("Toronto"))
