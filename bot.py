import discord
import csv
import asyncio
import datetime
import PUBGstats

global playingMembers, gamesIDs, PUBG 
playingMembers, gamesIDs = {}, set()
PUBG = "PLAYERUNKNOWN'S BATTLEGROUNDS"

TOKEN = None
with open ('TOKENS.csv', 'r') as TOKENS:
    TOKENSreader = csv.reader(TOKENS)

    for key in TOKENSreader:
        #print(key[0])
        if key[0] == 'discordPUBGbot':
            TOKEN = key[1]


if TOKEN == None:
    raise Exception('TOKEN not found, aborting...')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith('check'):
        print('-------------------')
        getPlayingMembers(client.get_all_members())
        print('current members: {}'.format(playingMembers))
        print('current game IDs: {}'.format(gamesIDs))
        print('-------------------')
        await trackPUBGRounds()
        print('-------------------')
    elif message.content.startswith('2check'):
        print('-------------------')
        getPlayingMembers(client.get_all_members())
        print('current members: {}'.format(playingMembers))
        print('current game IDs: {}'.format(gamesIDs))
        print('-------------------')

    elif message.content.startswith('who is the best player in the world?'):
        await message.channel.send('Lionel Messi')
    elif message.content.startswith('!top3'):
        # TODO make TOP3 depends on who requested it
        top3 = PUBGstats.getTopThreeKillRank()
        string = '#1: {} with {} kills\n #2: {} with {} kills\n #3: {} with {} kills'.format(top3[0][0], top3[0][1], top3[1][0], top3[1][1], top3[2][0], top3[2][1])
        await message.channel.send(string)
    elif message.content.startswith('bye'):
        await message.channel.send('logging out!')
        await client.logout()
    #ch = message.channel
    #print(type(ch))
    #await ch.send('hi')
    '''
    channel = client.get_channel(591227619928702979)
    print(channel)
    await channel.send('test')
    '''

async def reportDuo():

    while True:
        # TODO make this a global variable AFTER connecting to server
        channel = client.get_channel(595459764348125194)
        if channel == None:
            await asyncio.sleep(5)
            continue
        print(channel)
        result = PUBGstats.fetchDuoGame()
        if result != False:
            P1, P2 = result
            # TODO This works ONLY for duo, logic needs replacing if this tool is going to cover the other modes
            if P1 != None and P2 != None:
                embed = makeEmbed(P1, P2)
            else:
                result = False
        if channel != None and result != False:
            await channel.send('After Action Report Is Ready For Deployment! [BETA/TESTING][v0.1.5]')
            await channel.send(embed=embed)
        # wait for x amount of seconds to allow other tasks to be done,
        # then comeback and continue to do work with PUBG api
        await asyncio.sleep(60)

def makeEmbed(P1, P2):

    #print(P1)
    #print(P2)
    
    if P1['win-rank'] != P2['win-rank']:
        raise Exception('The ranks of P1 and P2 does not match [duo], aborting...')

    #TODO do the same for player 2
    originalP1 = P1.copy()
    P1 = formatLog(P1)
    originalP2= P2.copy()
    P2 = formatLog(P2)


    #TODO fix the timestamp. Update: test the new modification
    date = datetime.datetime.utcnow()#+datetime.timedelta(hours=0)
    #embed = discord.Embed(colour=discord.Colour(0xD0650A), description="Duo game with player1 and player2", timestamp=date)
    embed = discord.Embed(colour=discord.Colour(0xF8B547), description="Duo game with {} and {}".format(P1['name'], P2['name']), timestamp=date)
    embed.set_thumbnail(url="https://seeklogo.com/images/W/winner-winner-chicken-dinner-pubg-logo-A8CF2AD8D2-seeklogo.com.png")
    embed.set_author(name="Post Round Report")
    #embed.set_footer(text="This tool is developed by Suli", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text="This tool is developed by Suli", icon_url="https://i.ibb.co/7GL5pTM/STX-OFFCIAL-LOGO.png")

    x = 1000
    #embed.add_field(name="​", value="​") if spaces were ever needed
    embed.add_field(value="**Team rank: {}**".format(P1['win-rank']), name="\u200B", inline = False)

    embed.add_field(name="**{}**".format(P1['name']), value="**kills:  {}**\n**headshots: {}**\n**assists: {}**\n**knocks: {}**\n**revives: {}**\n**heals: {}**\n**boosts: {}**\n**walk distance: {}{unitWalk}\nkill rank: {}**\n**weapons acquired: {}**\n**time survived: {}{timeUnit}**\n**damage dealt: {}**\n**longest kill: {}m**\n**kill streak: {}**".format(P1['kills'], P1['headshots'], P1['assists'], P1['knocks'], P1['revives'], P1['heals'], P1['boosts'], P1['walk-distance'], P1['kill-rank'], P1['weapons-acquired'], P1['time-survived'], P1['damage-dealt'], P1['longest-kill'], P1['kill-streak'], unitWalk='km' if originalP1['walk-distance'] >= 1000 else 'm', timeUnit='m' if originalP1['time-survived'] >= 60 else 's'), inline=True)

    embed.add_field(name="**{}**".format(P2['name']), value="**kills:  {}**\n**headshots: {}**\n**assists: {}**\n**knocks: {}**\n**revives: {}**\n**heals: {}**\n**boosts: {}**\n**walk distance: {}{unitWalk}\nkill rank: {}**\n**weapons acquired: {}**\n**time survived: {}{timeUnit}**\n**damage dealt: {}**\n**longest kill: {}m**\n**kill streak: {}**".format(P2['kills'], P2['headshots'], P2['assists'], P2['knocks'], P2['revives'], P2['heals'], P2['boosts'], P2['walk-distance'], P2['kill-rank'], P2['weapons-acquired'], P2['time-survived'], P2['damage-dealt'], P2['longest-kill'], P2['kill-streak'], unitWalk='km' if originalP2['walk-distance'] >= 1000 else 'm', timeUnit='m' if originalP2['time-survived'] >= 60 else 's'), inline=True)
    return embed

def formatLog(log):

    if log['walk-distance'] >= 1000:
        log['walk-distance'] = log['walk-distance']/1000
    log['walk-distance'] = round(log['walk-distance'], 2)
    
    if log['time-survived'] >= 60:
        log['time-survived'] = log['time-survived']/60
    log['time-survived'] = round(log['time-survived'], 2)

    log['damage-dealt'] = int(log['damage-dealt'])
    log['longest-kill'] = round(log['longest-kill'], 2)
    return log

def getPlayingMembers(members):
    

    global playingMembers, gamesIDs 
    #print(bool(playingMembers))
    for member in members:
        print(member.name)
        #print(member.status)
        #print(type(str(member.status)))

        #TODO make gameName here
        # and if return is None then exit

        if member.name in playingMembers:
            if len(member.activities) == 0:
                del playingMembers[member.name]
            else:
                print('check if in PUBG or not')
                for activity in member.activities:
                    print(activity.name)
                    print(type(activity))
                    isPlaying = False
                    if activity.name == PUBG:
                        isPlaying = True 
                        break 
                #print('after for loop') 
                if isPlaying == False:
                    del playingMembers[member.name]

            continue 

        if member.bot == True or str(member.status) == 'offline' or len(member.activities) == 0:
            print('continue hit')
            continue
        #print(member)

        # If the program logic reached this stage
        # then it means that a new player has been
        # found

        for activity in member.activities:
            if activity.name == PUBG:
                gameName = getPUBGName(member.name)
                PUBGstats.getPlayerInfo(gameName)
                matchID = PUBGstats.getLatestMatchID(gameName)
                #print(gameName)
                playingMembers[member.name] = matchID
                gamesIDs.add(matchID)
                break 
        '''
        gameName = getPUBGName(member.name)
        matchID = PUBGstats.getLatestMatchID(gameName)
        #print(gameName)
        playingMembers[member.name] = matchID
        gamesIDs.add(matchID)
        '''
 
    
    #print(bool(playingMembers))
    #print(playingMembers)

# TODO make this a csv file that can be altered from the discord server
def getPUBGName(name):
    
    if name == 'suli':
        return 'stx0'
    elif name == 'jok':
        return 'kojx'
    else:
        return None

async def trackPUBGRounds():

    channel = client.get_channel(595459764348125194)
    if channel == None:
        await asyncio.sleep(5)
        channel = client.get_channel(595459764348125194)

    while True:
        getPlayingMembers(client.get_all_members())
        print('===========================================')
        print('before: {}'.format(playingMembers))
        for player in playingMembers.keys():
            print('member: {}'.format(player))
            gameName = getPUBGName(player)

            if gameName == None:
                print('continue hit 2')
                continue
           
            PUBGstats.getPlayerInfo(gameName)
            currentMatchID = PUBGstats.getLatestMatchID(gameName)

            # if player hasn't played a new game 
            # then do nothing OR if the game already
            # has been reported (only happens in duo & squad)
            if playingMembers[player] == currentMatchID or currentMatchID in gamesIDs:
                if currentMatchID in gamesIDs:
                    playingMembers[player] = currentMatchID
                    print('continue hit 3')
                else:
                    print('continue hit 4')
                continue
            
            # TODO make this the last thing to be made
            gamesIDs.add(currentMatchID)
            playingMembers[player] = currentMatchID
            print('current match ID: {}'.format(currentMatchID))

            roundType = PUBGstats.getRoundType(gameName)
            print(roundType)

            # TODO cover tpp as well
            if roundType == 'solo-fpp':
                print('temp')
                P1 = PUBGstats.matchAnalysis(gameName)
                embed = makeEmbedSolo(P1)
                await channel.send('After Action Report Is Ready For Deployment! [BETA/TESTING][v0.2.5]')
                await channel.send(embed=embed)
                #continue
            elif roundType == 'duo-fpp':
                print('temp duo')
                P1 = PUBGstats.matchAnalysis(gameName)
                P2name = PUBGstats.getTeamMembersNames(P1['name'], P1['win-rank'], 'duo')
                P2 = PUBGstats.matchAnalysis(P2name)
                embed = makeEmbedDuo(P1, P2)
                await channel.send('After Action Report Is Ready For Deployment! [BETA/TESTING][v0.2.5]')
                await channel.send(embed=embed)

            elif roundType == 'squad-fpp':
                print('temp squad')
            else:
                # if the game isn't solo, duo or squad (ex: war mode)
                # then don't report and move on to the next playing player
                continue

        print('after: {}'.format(playingMembers))
        print('waiting for 60 seconds')
        await asyncio.sleep(60)

def makeEmbedSolo(P1):

    originalP1 = P1.copy()
    P1 = formatLog(P1)


    #TODO fix the timestamp. Update: test the new modification
    date = datetime.datetime.utcnow()#+datetime.timedelta(hours=0)
    #embed = discord.Embed(colour=discord.Colour(0xD0650A), description="Duo game with player1 and player2", timestamp=date)
    embed = discord.Embed(colour=discord.Colour(0xF8B547), description="Solo game with {}".format(P1['name']), timestamp=date)
    embed.set_thumbnail(url="https://seeklogo.com/images/W/winner-winner-chicken-dinner-pubg-logo-A8CF2AD8D2-seeklogo.com.png")
    embed.set_author(name="Post Round Report")
    #embed.set_footer(text="This tool is developed by Suli", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text="This tool is developed by Suli", icon_url="https://i.ibb.co/7GL5pTM/STX-OFFCIAL-LOGO.png")

    x = 1000
    #embed.add_field(name="​", value="​") if spaces were ever needed
    embed.add_field(value="**Team rank: {}**".format(P1['win-rank']), name="\u200B", inline = False)

    embed.add_field(name="**{}**".format(P1['name']), value="**kills:  {}**\n**headshots: {}**\n**assists: {}**\n**knocks: {}**\n**revives: {}**\n**heals: {}**\n**boosts: {}**\n**walk distance: {}{unitWalk}\nkill rank: {}**\n**weapons acquired: {}**\n**time survived: {}{timeUnit}**\n**damage dealt: {}**\n**longest kill: {}m**\n**kill streak: {}**".format(P1['kills'], P1['headshots'], P1['assists'], P1['knocks'], P1['revives'], P1['heals'], P1['boosts'], P1['walk-distance'], P1['kill-rank'], P1['weapons-acquired'], P1['time-survived'], P1['damage-dealt'], P1['longest-kill'], P1['kill-streak'], unitWalk='km' if originalP1['walk-distance'] >= 1000 else 'm', timeUnit='m' if originalP1['time-survived'] >= 60 else 's'), inline=True)
    return embed

def makeEmbedDuo(P1, P2):

    originalP1 = P1.copy()
    P1 = formatLog(P1)
    originalP2= P2.copy()
    P2 = formatLog(P2)


    #TODO fix the timestamp. Update: test the new modification
    date = datetime.datetime.utcnow()#+datetime.timedelta(hours=0)
    #embed = discord.Embed(colour=discord.Colour(0xD0650A), description="Duo game with player1 and player2", timestamp=date)
    embed = discord.Embed(colour=discord.Colour(0xF8B547), description="Duo game with {} and {}".format(P1['name'], P2['name']), timestamp=date)
    embed.set_thumbnail(url="https://seeklogo.com/images/W/winner-winner-chicken-dinner-pubg-logo-A8CF2AD8D2-seeklogo.com.png")
    embed.set_author(name="Post Round Report")
    #embed.set_footer(text="This tool is developed by Suli", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text="This tool is developed by Suli", icon_url="https://i.ibb.co/7GL5pTM/STX-OFFCIAL-LOGO.png")

    x = 1000
    #embed.add_field(name="​", value="​") if spaces were ever needed
    embed.add_field(value="**Team rank: {}**".format(P1['win-rank']), name="\u200B", inline = False)

    embed.add_field(name="**{}**".format(P1['name']), value="**kills:  {}**\n**headshots: {}**\n**assists: {}**\n**knocks: {}**\n**revives: {}**\n**heals: {}**\n**boosts: {}**\n**walk distance: {}{unitWalk}\nkill rank: {}**\n**weapons acquired: {}**\n**time survived: {}{timeUnit}**\n**damage dealt: {}**\n**longest kill: {}m**\n**kill streak: {}**".format(P1['kills'], P1['headshots'], P1['assists'], P1['knocks'], P1['revives'], P1['heals'], P1['boosts'], P1['walk-distance'], P1['kill-rank'], P1['weapons-acquired'], P1['time-survived'], P1['damage-dealt'], P1['longest-kill'], P1['kill-streak'], unitWalk='km' if originalP1['walk-distance'] >= 1000 else 'm', timeUnit='m' if originalP1['time-survived'] >= 60 else 's'), inline=True)

    embed.add_field(name="**{}**".format(P2['name']), value="**kills:  {}**\n**headshots: {}**\n**assists: {}**\n**knocks: {}**\n**revives: {}**\n**heals: {}**\n**boosts: {}**\n**walk distance: {}{unitWalk}\nkill rank: {}**\n**weapons acquired: {}**\n**time survived: {}{timeUnit}**\n**damage dealt: {}**\n**longest kill: {}m**\n**kill streak: {}**".format(P2['kills'], P2['headshots'], P2['assists'], P2['knocks'], P2['revives'], P2['heals'], P2['boosts'], P2['walk-distance'], P2['kill-rank'], P2['weapons-acquired'], P2['time-survived'], P2['damage-dealt'], P2['longest-kill'], P2['kill-streak'], unitWalk='km' if originalP2['walk-distance'] >= 1000 else 'm', timeUnit='m' if originalP2['time-survived'] >= 60 else 's'), inline=True)
    return embed

#client.loop.create_task(reportDuo())
client.loop.create_task(trackPUBGRounds())
client.run(TOKEN)


#print(client.user)
