#! python

# Hyperion NHL Red Light System
# This program checks the website for live NHL Game Scores and if the preferred team (myTeam) scores then
# call the nhlGoal routine to flash the lights and play the horn
# created by PMC 20171009

# Import routines used in this program
import urllib2, json
import time
import nhlGoal
from datetime import datetime
from datetime import timedelta

#assign class modules
class gameInfo():
    gameFound = False
    myTeamScore = None
    myTeamLocation =''
    homeTeam =''
    awayTeam =''
    startTime = ''
    startDay = ''
    homeScore = None
    awayScore = None

#define global variabls
anounceDelay = 5 #time after a goal is detected to set the lights, to adjust for broadcast delays
debug = False
liveGame = False
updateTime = 1200 #initial time to check the website (10 minutes)
myGameInfo = gameInfo()
myLastScore = 0
myTeam = 'Toronto'  # 'Columbus'#'Nashville'#'Boston'#'Toronto'
url = "http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp"

#parse the web data and check for team information
def getGameData():
    tmpGameInfo = gameInfo()
    data = urllib2.urlopen(url).read()
    jsonData =  data[15:-1]
    try:
    	output = json.loads(jsonData)
    except:
	print 'Error processing Json File'
    gameList = output['games']
    # Evaluate each game in the list
    for game in gameList:
        if type(game) is dict:
            # Evaluate each key in the game
            for keyValue in game:
                myKeyName = keyValue
                if isinstance(game[keyValue],bool):
                    myKeyValue = 'True'
                elif isinstance(game[keyValue], int):
                    myKeyValue = str(game[keyValue])
                else:
                    myKeyValue = game[keyValue]
                if debug:
                    print myKeyName +' : ' + myKeyValue
                if myKeyName == 'atn':
                    tmpGameInfo.awayTeam = myKeyValue
                    if tmpGameInfo.awayTeam == myTeam:
                        tmpGameInfo.myTeamLocation = 'away'
                elif myKeyName == 'htn':
                    tmpGameInfo.homeTeam = myKeyValue
                    if tmpGameInfo.homeTeam == myTeam:
                        tmpGameInfo.myTeamLocation = 'home'
                elif myKeyName == 'bs':
                    tmpGameInfo.startTime = myKeyValue
                elif myKeyName == 'ts':
                    tmpGameInfo.startDay = myKeyValue
		    #print tmpGameInfo.startDay
                elif myKeyName == 'ats':
                    if myKeyValue <> "":
                        tmpGameInfo.awayScore = int(myKeyValue)
                    else:
                        tmpGameInfo.awayScore = 0
                elif myKeyName == 'hts':
                    if myKeyValue <> "":
                        tmpGameInfo.homeScore = int(myKeyValue)
                    else:
                        tmpGameInfo.homeScore = 0
        #now that we have populated the game info from the current game in gamelist
        #evaluate if it is the gaem we are looking for
        if (tmpGameInfo.homeTeam == myTeam or tmpGameInfo.awayTeam == myTeam):
            #check if game is in progress or not
            if (tmpGameInfo.startDay =="PRE GAME") and (tmpGameInfo.startTime =="LIVE"):
                #if we are in the pregame then begin checking website every minute
                print 'Game is in PreGame'
                print tmpGameInfo.startTime
                #print str(tmpGameInfo.startTime)[3:1]# + timedelta(hours=3)
                global updateTime
                updateTime = 120
                global liveGame
                liveGame = False
            elif (tmpGameInfo.startTime =="LIVE"):
                #if the game is active then begin checking the website every 5 seconds
                print 'Game is Live'
                #global updateTime
                updateTime = 5
                #global liveGame
                liveGame = True
            elif (tmpGameInfo.startTime =="FINAL"):
                #The game found in the record has already completed
                updateTime = 900
                liveGame = False
            elif (tmpGameInfo.startTime =="TODAY"):
                #The game found in the record has already completed
                updateTime = 900
                liveGame = False
            else:
                # if the game is active then begin checking the website every 5 minutes
                'Game is not pending'
                #global updateTime
                updateTime = 1200
                #global liveGame
                liveGame = False
                print 'Game Found'
                print tmpGameInfo.startDay
                print tmpGameInfo.startTime# + timedelta(hours=3)
            if liveGame:
                # since the game is live, prepare the myGameInfo to be used to check the scores
                tmpGameInfo.gameFound = True
                if tmpGameInfo.myTeamLocation == 'home':
                    tmpGameInfo.myTeamScore = tmpGameInfo.homeScore
                elif tmpGameInfo.myTeamLocation == 'away':
                    tmpGameInfo.myTeamScore = tmpGameInfo.awayScore
                global myGameInfo
                myGameInfo = tmpGameInfo
                #print myGameInfo.startDay
                #print myGameInfo.startTime
                #print myGameInfo.homeTeam
                #print myGameInfo.homeScore
                #print myGameInfo.awayTeam
                #print myGameInfo.awayScore
                break
            break
        else:
            tmpGameInfo.gameFound = False

            #print 'Game containing '+myTeam+' was not found'
            #global updateTime
            updateTime = 1200
        #global myGameInfo
        myGameInfo.gameFound = tmpGameInfo.gameFound




# This routine compares the game data found in the getGameData routine to see if myTeam scored since last check
def checkScore():
    global myLastScore
    print myTeam +' had: ' + str(myLastScore) + ' goals'
    if myGameInfo.myTeamScore <> myLastScore:
        myLastScore = myGameInfo.myTeamScore
	time.sleep(anounceDelay)
        nhlGoal.scored()
    else:
        global updateTime
        updateTime = 5
        #donothing
        #print 'No Change in Score'
    print myTeam + ' now has: ' +str(myLastScore)+ ' goals'


# loop the routine
while True:
    getGameData()
    if myGameInfo.gameFound and liveGame:
        checkScore()
    else:
        print "The " + myTeam + " game is not currently live."
        #print "Current Game Status: " +myGameInfo.startTime
        print "Waiting " + str(updateTime) + " seconds before checking again. "+time.strftime("%H:%M:%S")
    time.sleep(updateTime)



