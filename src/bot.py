import discord
import os
from get_all import *
import re
from dotenv import load_dotenv
from discord.ext import commands, tasks
from utils import searchSong
from ytdl import YTDLSource


load_dotenv('../.env')
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix='/', intents=intents)


all_songs = filtered_songs()[["title", "artist", "top genre"]]


def random_ten():
    ten_random_songs = (all_songs.sample(
        frac=1).groupby('top genre').head(1)).sample(10)
    return ten_random_songs


@client.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@client.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command(name='play_song', help='To play song')
async def play(ctx):
    user_message = str(ctx.message.content)
    song_name = user_message.split(' ', 1)[1]
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client
        url = searchSong(song_name)
        print(url)
        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=client.loop)
            voice_channel.play(discord.FFmpegPCMAudio(source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    except Exception as e:
        print(e)
        await ctx.send("The bot is not connected to a voice channel.")


@client.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@client.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")


@client.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@client.event
async def on_ready():
    for guild in client.guilds:
        print(guild.name)

        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

    bot_message = "Select songs by typing in the serial number: " + \
        "\n" + "-------------------------------------------------"
    i = 0
    ten_random_songs = random_ten()
    for ele in zip(ten_random_songs["title"], ten_random_songs["artist"]):
        bot_message += "\n" + str(i) + " " + str(ele[0]) + " By " + str(ele[1])
        i += 1

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
        else:
            await on_ready()
        await client.process_commands(message)

client.run(TOKEN)
