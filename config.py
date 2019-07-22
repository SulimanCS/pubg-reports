import csv
import os


global DISCORDCONFIGFILE
DISCORDCONFIGFILE = 'DISCORDCONFIG.csv'
directory = os.path.dirname(__file__)
filepath = os.path.join(directory, DISCORDCONFIGFILE)

def setRegistrationChannelID():
    
    ID = input('Please enter the channel ID for registering new users: ')
    with open(filepath, 'r') as CONFIG:
        CONFIGreader = csv.reader(CONFIG)
        lists = list(CONFIGreader)
        for line in lists:
            if line[0] == 'registration':
                line[1] = ID
        
        with open(filepath, 'w') as wCONFIG:
            CONFIGwriter = csv.writer(wCONFIG)
            CONFIGwriter.writerows(lists)

def setSoloChannelID():
    
    ID = input('Please enter the channel ID for reporting solo PUBG rounds: ')
    with open(filepath, 'r') as CONFIG:
        CONFIGreader = csv.reader(CONFIG)
        lists = list(CONFIGreader)
        for line in lists:
            if line[0] == 'soloReport':
                line[1] = ID
        
        with open(filepath, 'w') as wCONFIG:
            CONFIGwriter = csv.writer(wCONFIG)
            CONFIGwriter.writerows(lists)

def setDuoChannelID():
    
    ID = input('Please enter the channel ID for reporting duo PUBG rounds: ')
    with open(filepath, 'r') as CONFIG:
        CONFIGreader = csv.reader(CONFIG)
        lists = list(CONFIGreader)
        for line in lists:
            if line[0] == 'duoReport':
                line[1] = ID
        
        with open(filepath, 'w') as wCONFIG:
            CONFIGwriter = csv.writer(wCONFIG)
            CONFIGwriter.writerows(lists)

def setSquadChannelID():
    
    ID = input('Please enter the channel ID for reporting squad PUBG rounds: ')
    with open(filepath, 'r') as CONFIG:
        CONFIGreader = csv.reader(CONFIG)
        lists = list(CONFIGreader)
        for line in lists:
            if line[0] == 'squadReport':
                line[1] = ID
        
        with open(filepath, 'w') as wCONFIG:
            CONFIGwriter = csv.writer(wCONFIG)
            CONFIGwriter.writerows(lists)

