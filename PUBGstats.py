import requests 
import json
import csv
from datetime import datetime


def getToken():

    TOKEN = None

    with open ('TOKENS.csv', 'r') as TOKENS:

        TOKENSreader = csv.reader(TOKENS)

        for key in TOKENSreader:
            #print(key[0])
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
    print(url)

    r = requests.get(url, headers=header)
    if r.ok == False:
        return
    r_dict = r.json()

    #print(r.json())
    #print(type(r_dict))

    filename = player + '.json'
    filename = 'playerdata/' + filename
    
    #with open ('playerdata/data.json', 'w') as f:
    with open (filename, 'w') as f:
        json.dump(r_dict, f, indent=4)


def getLatestMatch(player):
    
    filename = player + '.json'
    filename = 'playerdata/' + filename
    with open (filename, 'r') as playerFile:
        playerData = json.load(playerFile)
        '''
        for info in playerData:
            print(info)
            #print(playerData['data'])
            for types in playerData['data']:
                print(types)
                test = types
        '''
    '''
    print('------------------------------')
    print(test['relationships']['matches'])
    matches = test['relationships']['matches']
    print('------------------------------')
    print(matches['data'][0]['id'])
    '''

    final = playerData['data'][0]['relationships']['matches']['data'][0]['id']
    print(final)

    return final
    
def getMatchInfo(matchID):

    url = 'https://api.pubg.com/shards/steam/matches/'
    url = url + matchID 
    print(url)

    r = requests.get(url, headers=header)
    if r.ok == False:
        return

    r_dict = r.json()

    filename = datetime.now().isoformat(timespec='minutes') + '.json'
    filename = 'matchdata/' + filename
    #with open ('playerdata/data.json', 'w') as f:
    with open (filename, 'w') as f:
        json.dump(r_dict, f, indent=4)
    

def matchAnalysis(player):
  
    log = {'name': None, 'kills': None, 'knocks': None, 'assists': None,
           'headshots': None, 'revives': None, 'heals': None,
           'boosts': None, 'walk-distance': None, 'kill-rank': None,
           'weapons-acquired': None, 'time-survived': None, 
           'damage-dealt': None, 'longest-kill': None, 'kill-streak': None,
           'win-rank': None}
           
    with open ('matchdata/test.json', 'r') as playerFile:
        playerData = json.load(playerFile)

        #for info in playerData:
            #print(info)
        #print(playerData['included'][0]['type'])
        # if participant, then check the name
        #print(playerData['included'][0]['attributes']['stats'])
        
        #print(len(playerData['included']))
        print('---------------------')
        for report in playerData['included']:
            #print(report['type'])
            if report['type']== 'participant':
                #print(True)
                print(report['attributes']['stats']['name'])
                if report['attributes']['stats']['name'] == player: 
                    #print('kills: {}'.format(report['attributes']['stats']['kills']))
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
            
#def checkNewMatch(player, currentMatchID):
#
#    matchID = getLatestMatch(player)
#    if matchID == currentMatchID:
#        return False
#    else:
#        return True
#

global matchID1, matchID2
matchID1 = '1' 
matchID2 = None
def testnewmatch():

    global matchID1, matchID2
    print('matchID1,2: {} and {}'.format(matchID1, matchID2))
    
    #matchID = '8199d282-4576-4d4e-9726-8a8dcfdb6c' 
    #return checkNewMatch('stx0', matchID)
    getPlayerInfo('stx0')
    getPlayerInfo('kojx')

    # store the match ID of the last played game
    # once it gets updated, we know that the players
    # entered a new game
    if matchID1 == None and matchID2 == None:
        matchID1 = getLatestMatch('stx0')
        matchID2 = getLatestMatch('kojx')
        print('YES')
        return

    currentMatchID1 = getLatestMatch('stx0')
    currentMatchID2 = getLatestMatch('kojx')
    
    # if current match ID matches with the previous
    # one then the players did not play a new match
    # therefore, return/exit
    if currentMatchID1 == matchID1 and currentMatchID2 == matchID2:
        print('YES2')
        return
    
    # if the routine survived the returns
    # then it means that the players entered
    # a new match

    # TODO this is for duos only currently
    # support for solo and squads will come
    # in the later versions

    # since players entered a new match
    # record their game stats and set 
    # the ID of the match
    logP1 = matchAnalysis('stx0')
    logP2 = matchAnalysis('kojx')
    matchID1 = currentMatchID1
    matchID2 = currentMatchID2
    return logP1, logP2


    

def main():

    #getPlayerInfo('stx0')
    #getPlayerInfo('kojx')
    #matchID1 = getLatestMatch('stx0')
    #matchID2 = getLatestMatch('kojx')

    #--------------------------

    #getPlayerInfo('stx0')
    #matchID = getLatestMatch('stx0')
    #getMatchInfo(matchID)
    #log = matchAnalysis('stx0')
    #print(log)

    #--------------------------

    result = testnewmatch()
    print('result is: {}'.format(result))
    result = testnewmatch()
    print('result is: {}'.format(result))




# init needs to be here when imported to another .py file
#init()

if __name__ == '__main__':

    init()
    main()
