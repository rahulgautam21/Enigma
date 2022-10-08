from multiprocessing.util import debug
import discord
import os
from get_all import *
import re
from dotenv import load_dotenv
from discord.ext import commands
from utils import searchSong
from songs_queue import Songs_Queue
from songs_cog import Songs


load_dotenv('../.env')
TOKEN = os.getenv('DISCORD_TOKEN')
# This can be obtained using ctx.message.author.voice.channel
VOICE_CHANNEL_ID = 1017135653789646851
intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix='/', intents=intents)


@client.event
async def on_ready():
    # for guild in client.guilds:
    #     print(guild.name)
    #     print(
    #         f'{client.user} is connected to the following guild:\n'
    #         f'{guild.name}(id: {guild.id})'
    #     )
    voice_channel = client.get_channel(VOICE_CHANNEL_ID)
    if client.user not in voice_channel.members:
        await voice_channel.connect()
    await client.load_extension("songs_cog")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    options = set()

    if message.channel.name == 'general':
        user_message = str(message.content)
        await client.process_commands(message)

client.run(TOKEN)
