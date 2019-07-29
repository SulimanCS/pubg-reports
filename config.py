import csv
import os


global DISCORDCONFIGFILE
DISCORDCONFIGFILE = 'DISCORDCONFIG.csv'
directory = os.path.dirname(__file__)
configFilepath = os.path.join(directory, DISCORDCONFIGFILE)

global TOKENSFILE 
TOKENSFILE = 'TOKENS.csv'
directory = os.path.dirname(__file__)
tokenFilepath = os.path.join(directory, TOKENSFILE)

def setRegistrationChannelID():
    
    ID = input('Please enter the channel ID for registering new users: ')
    with open(configFilepath, 'r') as CONFIG:
        CONFIGreader = csv.reader(CONFIG)
        lists = list(CONFIGreader)
        for line in lists:
            if line[0] == 'registration':
                line[1] = ID
        
        with open(configFilepath, 'w') as wCONFIG:
            CONFIGwriter = csv.writer(wCONFIG)
            CONFIGwriter.writerows(lists)

def setSoloChannelID():
    
    ID = input('Please enter the channel ID for reporting solo PUBG rounds: ')
    with open(configFilepath, 'r') as CONFIG:
        CONFIGreader = csv.reader(CONFIG)
        lists = list(CONFIGreader)
        for line in lists:
            if line[0] == 'soloReport':
                line[1] = ID
        
        with open(configFilepath, 'w') as wCONFIG:
            CONFIGwriter = csv.writer(wCONFIG)
            CONFIGwriter.writerows(lists)

def setDuoChannelID():
    
    ID = input('Please enter the channel ID for reporting duo PUBG rounds: ')
    with open(configFilepath, 'r') as CONFIG:
        CONFIGreader = csv.reader(CONFIG)
        lists = list(CONFIGreader)
        for line in lists:
            if line[0] == 'duoReport':
                line[1] = ID
        
        with open(configFilepath, 'w') as wCONFIG:
            CONFIGwriter = csv.writer(wCONFIG)
            CONFIGwriter.writerows(lists)

def setSquadChannelID():
    
    ID = input('Please enter the channel ID for reporting squad PUBG rounds: ')
    with open(configFilepath, 'r') as CONFIG:
        CONFIGreader = csv.reader(CONFIG)
        lists = list(CONFIGreader)
        for line in lists:
            if line[0] == 'squadReport':
                line[1] = ID
        
        with open(configFilepath, 'w') as wCONFIG:
            CONFIGwriter = csv.writer(wCONFIG)
            CONFIGwriter.writerows(lists)

def setPUBGToken():
    
    ID = input('Please enter the developer API TOKEN for PUBG: ')
    with open(tokenFilepath, 'r') as CONFIG:
        CONFIGreader = csv.reader(CONFIG)
        lists = list(CONFIGreader)
        for line in lists:
            if line[0] == 'PUBGapi':
                line[1] = ID
        
        with open(tokenFilepath, 'w') as wCONFIG:
            CONFIGwriter = csv.writer(wCONFIG)
            CONFIGwriter.writerows(lists)

def setDiscordToken():
    
    ID = input('Please enter the developer API TOKEN for the Discord bot: ')
    with open(tokenFilepath, 'r') as CONFIG:
        CONFIGreader = csv.reader(CONFIG)
        lists = list(CONFIGreader)
        for line in lists:
            if line[0] == 'discordPUBGbot':
                line[1] = ID
        
        with open(tokenFilepath, 'w') as wCONFIG:
            CONFIGwriter = csv.writer(wCONFIG)
            CONFIGwriter.writerows(lists)
            
def configChannels():

    setRegistrationChannelID()
    setSoloChannelID()
    setDuoChannelID()
    setSquadChannelID()

def configTokens():

    setDiscordToken()
    setPUBGToken()

def configAll():

    setDiscordToken()
    setPUBGToken()
    setRegistrationChannelID()
    setSoloChannelID()
    setDuoChannelID()
    setSquadChannelID()

