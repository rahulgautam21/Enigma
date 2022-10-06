from multiprocessing.util import debug
import discord
import os
from get_all import *
import re
from dotenv import load_dotenv
from discord.ext import commands
from utils import searchSong
from songs_queue import Songs_Queue
import youtube_dl


load_dotenv('../.env')
TOKEN = os.getenv('DISCORD_TOKEN')
# This can be obtained using ctx.message.author.voice.channel
VOICE_CHANNEL_ID = 1017135653789646851
intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix='/', intents=intents)
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'True'}

all_songs = filtered_songs()[["title", "artist", "top genre"]]


def random_ten():
    ten_random_songs = (all_songs.sample(
        frac=1).groupby('top genre').head(1)).sample(10)
    return ten_random_songs


@client.command(name='play_song', help='To play song')
async def play(ctx):
    user_message = str(ctx.message.content)
    song_name = user_message.split(' ', 1)[1]
    await play_song(song_name, ctx)


async def play_song(song_name, ctx):
    # First stop whatever the bot is playing
    await stop(ctx)
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client
        url = searchSong(song_name)
        async with ctx.typing():
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                I_URL = info['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(I_URL, **FFMPEG_OPTIONS)
                voice_channel.play(source)
                voice_channel.is_playing()
        await ctx.send('**Now playing:** {}'.format(song_name))
    except Exception as e:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command(name='next_song', help='To play next song in queue')
async def play(ctx):
    try:
        songs_queue
    except NameError:
        await ctx.send("No recommendations present. First generate recommendations")
        return
    if songs_queue.get_len() == 0:
        await ctx.send("No recommendations present. First generate recommendations")
        return
    await play_song(songs_queue.next_song(), ctx)


@client.command(name='prev_song', help='To play prev song in queue')
async def play(ctx):
    try:
        songs_queue
    except NameError:
        await ctx.send("No recommendations present. First generate recommendations")
        return
    if songs_queue.get_len() == 0:
        await ctx.send("No recommendations present. First generate recommendations")
        return
    await play_song(songs_queue.prev_song(), ctx)


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
        voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


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


@client.command(name='poll', help='Poll for recommendation')
async def poll(ctx):
    reactions = ['👍', '👎']
    selected_songs = []
    count = 0
    bot_message = "Select song preferences by reaction '👍' or '👎' to the choices. \nSelect 3 songs"
    await ctx.send(bot_message)
    ten_random_songs = random_ten()
    for ele in zip(ten_random_songs["title"], ten_random_songs["artist"]):
        bot_message = str(ele[0]) + " By " + str(ele[1])
        description = []
        poll_embed = discord.Embed(
            title=bot_message, color=0x31FF00, description=''.join(description))
        react_message = await ctx.send(embed=poll_embed)
        for reaction in reactions[:len(reactions)]:
            await react_message.add_reaction(reaction)
        res, user = await client.wait_for('reaction_add')
        if (res.emoji == u'👍'):
            selected_songs.append(str(ele[0]))
            count += 1
        if (count == 3):
            bot_message = "Selected songs are : " + ' , '.join(selected_songs)
            await ctx.send(bot_message)
            break
    # TODO: Send the selected songs and get preferences
    # For now setting it manually
    global songs_queue
    songs_queue = Songs_Queue(ten_random_songs['title'].tolist())


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
