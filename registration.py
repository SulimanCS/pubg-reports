import csv
import PUBGstats

global filename
filename = 'PLAYERS.csv'

def checkRegistration(discordName, PUBGName):

    with open(filename, 'r') as fil:
        r = csv.reader(fil)
        next(r) # skip headers
        lineNum = 1
        for line in r:
            if line[0] == discordName:
                if line[1] == PUBGName:
                    return True
                else:
                    return lineNum
            lineNum+= 1
        return False

def registerPlayer(discordName, PUBGName):
    
    result = checkRegistration(discordName, PUBGName)

    isPUBGPlayer = PUBGstats.getPlayerInfo(PUBGName)
    #print(isPUBGPlayer)
    if isPUBGPlayer == False:
        result = -1

    # TODO check the case where to discord users
    # are set to the same game ID
    
    if result == True and isinstance(result, bool) == True:
        return 'User ({}) is already registered with the PUBG name ({})'.format(discordName, PUBGName)
    elif result == False:
        with open(filename, 'a') as fil:
            toAdd = [discordName, PUBGName]
            w = csv.writer(fil)
            w.writerows([toAdd])
            return 'User ({}) is now registered with the PUBG name ({})'.format(discordName, PUBGName)
    elif isinstance(result, int) == True and result > 0:
        with open(filename, 'r') as fil:
            r = csv.reader(fil)
            lists = list(r)
            oldPUBGName = lists[result][1] 
            lists[result][1] = PUBGName 
            with open(filename, 'w') as wfil:
                w = csv.writer(wfil)
                w.writerows(lists)
        return 'User ({}) PUBG name has been updated from ({}) to ({})'.format(discordName, oldPUBGName, PUBGName)
    elif result == -1:
            return "({}) is not a valid PUBG name (the player's profile has not been found on the PUBG servers)".format(PUBGName)
        
    else:
        return False

def getRegisteredPlayers():

    with open(filename, 'r') as fil:
        r = csv.reader(fil)
        next(r)
        players = list(r)

    return players



def main():

        
    # main is for testing purposes

    # TESTING checkRegistration, success
    '''
    result = checkRegistration('suli', 'stx0')
    print('case suli, stx0, result: {}'.format(result))
    result = checkRegistration('suli', 'none')
    print('case suli, none, result: {}'.format(result))
    result = checkRegistration('su', 'none')
    print('case su, none, result: {}'.format(result))
    '''
    # TESTING registerPlayer, success
    '''
    result = registerPlayer('suli', 'stx0')
    print('case suli, stx0, result: {}'.format(result))
    print('===========================')
    result = registerPlayer('suli', 'non')
    print('case suli, non, result: {}'.format(result))
    print('===========================')
    result = registerPlayer('su', 'non')
    print('case su, non, result: {}'.format(result))
    '''
    players = getRegisteredPlayers()
    return None


if __name__ == '__main__':
    main()
