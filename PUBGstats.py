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
            

def main():

    getPlayerInfo('stx0')
    matchID = getLatestMatch('stx0')
    getMatchInfo(matchID)
    log = matchAnalysis('stx0')
    print(log)


# init needs to be here when imported to another .py file
#init()

if __name__ == '__main__':

    init()
    main()
