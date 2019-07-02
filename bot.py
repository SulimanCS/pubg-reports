import discord
import csv
import asyncio
import datetime
import PUBGstats

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
    elif message.content.startswith('who is the best player in the world?'):
        await message.channel.send('Lionel Messi')
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

async def test():
   
    #result = PUBGstats.testnewmatch()
    #if result == False:
    #    return
    #P1, P2 = result
    #print (P1)
    #print (P2)
    #embed = makeEmbed(P1, P2)
    #return
    ''' old embed
    #TODO fix the timestamp
    date = datetime.datetime.now()
    #embed = discord.Embed(colour=discord.Colour(0xD0650A), description="Duo game with player1 and player2", timestamp=date)
    embed = discord.Embed(colour=discord.Colour(0xF8B547), description="Duo game with player1 and player2", timestamp=date)
    embed.set_thumbnail(url="https://seeklogo.com/images/W/winner-winner-chicken-dinner-pubg-logo-A8CF2AD8D2-seeklogo.com.png")
    embed.set_author(name="Post Round Report")
    embed.set_footer(text="This tool is developed by Suli", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

    #embed.add_field(name="​", value="​")
    embed.add_field(value="**Team rank: x**", name="\u200B", inline = False)
    embed.add_field(name="**P1**", value="**kills:\t\t x**\n**headshots: x**\n**assists:   x**\n**knocks:   x**\n**revives:  x**\n**heals:     x**\n**boosts:   x**\n**walk distance:  x\nkill rank:   x**\n**weapons acquired:   x**", inline=True)
    embed.add_field(name="**P2**", value="**kills:\t\t x**\n**headshots: x**\n**assists:   x**\n**knocks:   x**\n**revives:  x**\n**heals:     x**\n**boosts:   x**\n**walk distance:  x\nkill rank:   x**\n**weapons acquired:   x**", inline=True)
    #embed.add_field(name="**P2**", value="**kills:\t\t x**\n**assists:   x**\n**knocks:   x**", inline=True)
    '''

    # TODO change the channel to the new channel later
    while True:
        #print('hi')
        #channel = client.get_channel(595458801960747008)
        channel = client.get_channel(595459764348125194)
        if channel == None:
            await asyncio.sleep(5)
            continue
        #print(channel)
        result = PUBGstats.testnewmatch()
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

    
        



client.loop.create_task(test())
client.run(TOKEN)


#print(client.user)
