import discord
import csv
import asyncio
import datetime

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
    channel = client.get_channel(591227619928702979)
    print(channel)
    await channel.send('test')

async def test():
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
    while True:
        print('hi')
        channel = client.get_channel(591227619928702979)
        print(channel)
        if channel != None:
            await channel.send('After Action Report Is Ready For Deployment! [TESTING]')
            await channel.send(embed=embed)
        # wait for x amount of seconds to allow other tasks to be done,
        # then comeback and continue to do work with PUBG api
        await asyncio.sleep(5)

client.loop.create_task(test())
client.run(TOKEN)


#print(client.user)
