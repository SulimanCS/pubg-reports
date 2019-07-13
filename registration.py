import csv
import PUBGstats

global filename
filename = 'PLAYERS.csv'

def checkRegistration(discordName, playerName):

    with open(filename, 'r') as fil:
        r = csv.reader(fil)
        next(r) # skip headers
        lineNum = 1
        for line in r:
            if line[0] == discordName:
                if line[1] == playerName:
                    return True
                else:
                    return lineNum
            lineNum+= 1
        return False
    

def main():

        
    # main is for testing purposes
    result = checkRegistration('suli', 'stx0')
    print('case suli, stx0, result: {}'.format(result))
    result = checkRegistration('suli', 'none')
    print('case suli, none, result: {}'.format(result))
    result = checkRegistration('su', 'none')
    print('case su, none, result: {}'.format(result))
    return None


if __name__ == '__main__':
    main()
