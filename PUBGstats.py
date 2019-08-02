import requests 
import json
import csv
from datetime import datetime
import os
import glob

global TOKENSFILE
TOKENSFILE = 'TOKENS.csv'

global PLAYERDATA, MATCHDATA
PLAYERDATA, MATCHDATA = 'playerdata', 'matchdata'

def getToken():

    TOKEN = None
    
    directory = os.path.dirname(__file__)
    filepath = os.path.join(directory, TOKENSFILE)
    with open (filepath, 'r') as TOKENS:

        TOKENSreader = csv.reader(TOKENS)

        for key in TOKENSreader:
            if key[0] == 'PUBGapi':
                TOKEN = key[1]

    if TOKEN == None:
        raise Exception('TOKEN not found, aborting...')

    return TOKEN

def init():

    global TOKEN
    global header

    TOKEN = getToken()
    header = {
      "Authorization": "Bearer " + TOKEN,
      "Accept": "application/vnd.api+json",
      "Accept-Encoding": "gzip"
    }
   
def getPlayerInfo(player):
    
    url = 'https://api.pubg.com/shards/steam/players?filter[playerNames]='
    url = url + player

    r = requests.get(url, headers=header)
    
    if r.ok == False:
        return False
    r_dict = r.json()

    filename = player + '.json'
    directory = os.path.dirname(__file__)
    filepath = os.path.join(directory, PLAYERDATA, filename)
    
    with open (filepath, 'w') as f:
        json.dump(r_dict, f, indent=4)

    return r_dict

def getLatestMatchID(playerProfile):

    playerData = playerProfile
    
    try:
        final = playerData['data'][0]['relationships']['matches']['data'][0]['id']
    except IndexError as error:
        print('Player ({}) has not played a single PUBG game yet, error: {}'.format(playerData['data'][0]['attributes']['name'], error))
        final = None

    return final
    
def getMatchInfo(matchID):

    url = 'https://api.pubg.com/shards/steam/matches/'
    url = url + matchID 

    r = requests.get(url, headers=header)
    if r.ok == False:
        return

    r_dict = r.json()

    filename = matchID + '.json'
    directory = os.path.dirname(__file__)
    filepath = os.path.join(directory, MATCHDATA, filename)

    with open (filepath, 'w') as f:
        json.dump(r_dict, f, indent=4)

    return r_dict
    
def getLastModfiedMatchFile():

    directory = os.path.dirname(__file__)
    filepaths = os.path.join(directory, MATCHDATA, '*.json')
    files = glob.glob(filepaths)

    return max(files, key=os.path.getctime)
    
def matchAnalysis(player, matchData):
  
    log = {'name': None, 'kills': None, 'knocks': None, 'assists': None,
           'headshots': None, 'revives': None, 'heals': None,
           'boosts': None, 'walk-distance': None, 'kill-rank': None,
           'weapons-acquired': None, 'time-survived': None, 
           'damage-dealt': None, 'longest-kill': None, 'kill-streak': None,
           'win-rank': None}
   
    for report in matchData['included']:
        if report['type']== 'participant':
            if report['attributes']['stats']['name'] == player: 
                log['name'] = report['attributes']['stats']['name']
                log['kills'] = report['attributes']['stats']['kills']
                log['knocks'] = report['attributes']['stats']['DBNOs']
                log['assists'] = report['attributes']['stats']['assists']
                log['headshots'] = report['attributes']['stats']['headshotKills']
                log['revives'] = report['attributes']['stats']['revives']
                log['heals'] = report['attributes']['stats']['heals']
                log['boosts'] = report['attributes']['stats']['boosts']
                log['walk-distance'] = report['attributes']['stats']['walkDistance']
                log['kill-rank'] = report['attributes']['stats']['killPlace']
                log['weapons-acquired'] = report['attributes']['stats']['weaponsAcquired']
                log['time-survived'] = report['attributes']['stats']['timeSurvived']
                log['damage-dealt'] = report['attributes']['stats']['damageDealt']
                log['longest-kill'] = report['attributes']['stats']['longestKill']
                log['kill-streak'] = report['attributes']['stats']['killStreaks']
                log['win-rank'] = report['attributes']['stats']['winPlace']
                

                return log

def getTopThreeKillRank():

    try:
        newestFile = getLastModfiedMatchFile()
    except ValueError as error:
        print('no recent game file has been found, error: ', error)
        return False
    killLog = []
    P1, P2, P3 = None, None, None
    with open (newestFile, 'r') as playerFile:
        playerData = json.load(playerFile)
        for report in playerData['included']:
            if report['type'] == 'participant':
                if report['attributes']['stats']['killPlace'] == 1:
                    P1 = (report['attributes']['stats']['name'], report['attributes']['stats']['kills'])
                if report['attributes']['stats']['killPlace'] == 2:
                    P2 = (report['attributes']['stats']['name'], report['attributes']['stats']['kills'])
                if report['attributes']['stats']['killPlace'] == 3:
                    P3 = (report['attributes']['stats']['name'], report['attributes']['stats']['kills'])

    killLog.append(P1)
    killLog.append(P2)
    killLog.append(P3)

    return killLog

def getTopThreeKillRankUserSpecific(player):

    if player == None:
        return None
    killLog = []
    P1, P2, P3 = None, None, None
    matchData = getMatchInfo(getLatestMatchID(getPlayerInfo(player)))
    for report in matchData['included']:
        if report['type'] == 'participant':
            if report['attributes']['stats']['killPlace'] == 1:
                P1 = (report['attributes']['stats']['name'], report['attributes']['stats']['kills'])
            if report['attributes']['stats']['killPlace'] == 2:
                P2 = (report['attributes']['stats']['name'], report['attributes']['stats']['kills'])
            if report['attributes']['stats']['killPlace'] == 3:
                P3 = (report['attributes']['stats']['name'], report['attributes']['stats']['kills'])

    killLog.append(P1)
    killLog.append(P2)
    killLog.append(P3)

    return killLog

def getRoundType(matchData):

    gameMode = matchData['data']['attributes']['gameMode']
    return gameMode

def getMapName(matchData):
    
    mapName = matchData['data']['attributes']['mapName']
    return mapName
    
def getTeamMembersNames(player, mode, matchData):
    
    newestFile = getLastModfiedMatchFile()
    currentPlayerTeamID = None
    
    if mode == 'duo':
        for report in matchData['included']:
            if report['type']== 'participant':
                if report['attributes']['stats']['name'] == player:
                    currentPlayerTeamID = report['id']
                    break
        if currentPlayerTeamID == None:
            # if player not found, exit
            return None
        for report in matchData['included']:
            if report['type']== 'roster':
                if len(report['relationships']['participants']['data']) == 1:
                    if report['relationships']['participants']['data'][0]['id'] == currentPlayerTeamID:
                        # if team size in duo is equal to one player,
                        # then it means that the player doesn't have 
                        # a partner. It's rare in duo, but it happens
                        return None
                else: 
                    if report['relationships']['participants']['data'][0]['id'] == currentPlayerTeamID:
                        secondTeamMemberID = report['relationships']['participants']['data'][1]['id']
                        break
                    elif report['relationships']['participants']['data'][1]['id'] == currentPlayerTeamID:
                        secondTeamMemberID = report['relationships']['participants']['data'][0]['id']
                        break
        if secondTeamMemberID == None:
            return None
        for report in matchData['included']:
            if report['type']== 'participant':
                if report['id'] == secondTeamMemberID:
                   # other team member found, return the name
                   return report['attributes']['stats']['name']
    if mode == 'squad':
        for report in matchData['included']:
            if report['type']== 'participant':
                if report['attributes']['stats']['name'] == player:
                    currentPlayerTeamID = report['id']
                    break
        if currentPlayerTeamID == None:
            # if player not found, exit
            return None
        squad = None
        for report in matchData['included']:
            if report['type']== 'roster':
                if len(report['relationships']['participants']['data']) == 1:
                    if report['relationships']['participants']['data'][0]['id'] == currentPlayerTeamID:
                        # if team size in a squad is equal to one player,
                        # then it means that the player doesn't have 
                        # any partners
                        return None
                else:
                    for player in report['relationships']['participants']['data']:
                        if player['id'] == currentPlayerTeamID:
                            squad = report['relationships']['participants']['data']
                            break 
        if squad == None or len(squad) == 1:
            return None
        squadIDs = []
        for player in squad:
            if player['id'] == currentPlayerTeamID:
                continue
            squadIDs.append(player['id'])
        squadPlayerNames = []
        for report in matchData['included']:
            if report['type']== 'participant':
                if squadIDs == []:
                    # if all players are found,
                    # return their names, no need
                    # to loop through all players
                    return squadPlayerNames
                if report['id'] in squadIDs:
                    squadPlayerNames.append(report['attributes']['stats']['name'])
                    squadIDs.remove(report['id'])
        return squadPlayerNames
    else:
        return None
                        

def main():

    # main is for testing purposes

    #getPlayerInfo('stx0')
    #getPlayerInfo('kojx')
    #matchID1 = getLatestMatchID('stx0')
    #matchID2 = getLatestMatchID('kojx')

    #--------------------------

    #getPlayerInfo('stx0')
    #matchID = getLatestMatchID('stx0')
    #getMatchInfo(matchID)
    #log = matchAnalysis('stx0')
    #print(log)

    #--------------------------

    #result = fetchDuoGame()
    #print('result is: {}'.format(result))
    #print('\n\n=================================\n\n')
    #result = fetchDuoGame()
    #print('result is: {}'.format(result))

    #--------------------------

    #getLastModfiedMatchFile()
    #getMatchInfo(getLatestMatchID('stx0'))
    #getTopThreeKillRank()
    #getRoundType('stx0')

    #--------------------------
    
    #P1 = matchAnalysis('stx0')
    #print('=========111=======')
    #P2name = getTeamMembersNames(P1['name'], 'duo')
    #print(P2name)

    #--------------------------

    #getPlayerInfo('stx0')
    #print(getLatestMatchID('stx0'))
    #getMatchInfo(getLatestMatchID('stx0'))
    #print(getLastModfiedMatchFile())
    #print(matchAnalysis('stx0'))

    #--------------------------

    #print(getPlayerInfo('stx0'))
    #print(getLatestMatchID(getPlayerInfo('stx0')))
    #matchData = getMatchInfo(getLatestMatchID(getPlayerInfo('stx0')))
    #print(matchAnalysis('stx0', matchData))
    #print(getTeamMembersNames('stx0', 'duo', matchData))

    return None




# init needs to be here when imported to another .py file
#init()

if __name__ == '__main__':

    init()
    main()
else:
    init()
