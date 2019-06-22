import discord
import csv
import asyncio

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
        await message.channel.send('bye suli and jok!')
        await client.logout()
    #ch = message.channel
    #print(type(ch))
    #await ch.send('hi')
    channel = client.get_channel(591227619928702979)
    print(channel)
    await channel.send('test')

async def test():
    while True:
        print('hi')
        # wait for x amount of seconds to allow other tasks to be done,
        # then comeback and continue to do work with PUBG api
        await asyncio.sleep(5)

client.loop.create_task(test())
client.run(TOKEN)


#print(client.user)
