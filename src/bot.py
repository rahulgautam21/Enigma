import discord
import os
from get_all import *
import re
from dotenv import load_dotenv


load_dotenv('.env')
TOKEN = os.getenv('DISCORD_TOKEN')
# TOKEN = "MTAyMzc2MDAzNzIwMzY4MTI5MA.Gww-Na.W3xIuZd2Fcd_GwD7QEW0YWDFQqZyEkAL5vzeb4"
intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

all_songs = filtered_songs()[["title", "artist", "top genre"]]

def random_ten():
    ten_random_songs = (all_songs.sample(frac=1).groupby('top genre').head(1)).sample(10)
    return ten_random_songs

@client.event
async def on_ready():
    for guild in client.guilds:
        print(guild.name)

        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

    bot_message = "Select upto three songs by typing in the serial number: "
    i = 0
    ten_random_songs = random_ten()
    for ele in zip(ten_random_songs["title"], ten_random_songs["artist"]):
        bot_message += "\n" + str(i) + " " + str(ele[0]) + " By "+ str(ele[1])
        i+=1
    
    bot_message2 = "If you want to change the selection of songs, type in any alphabet"

    await client.get_channel(1017135653789646850).send(bot_message)
    await client.get_channel(1017135653789646850).send(bot_message2)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    options = set()

    if message.channel.name == 'general':
        user_message = str(message.content)
        options = set(re.findall(r'\d', user_message))
        if options:
            print(options)
        else :
            await on_ready()
            
client.run(TOKEN)