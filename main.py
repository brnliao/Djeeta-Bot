import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import youtube_dl

file = open("token.txt", 'r')
token = file.readline().split('\n')[0]
file.close()

Client = discord.Client()
client = commands.Bot(command_prefix = "?")


@client.event
async def on_ready():
    print("Bot is ready!")


@client.event
async def music_player(voice_channel, url):
    # load opus for the bot to play audio
    if not discord.opus.is_loaded():
        discord.opus.load_opus("libopus.so.1")

    server = voice_channel.server
    if not client.is_voice_connected(server):
        voice = await client.join_voice_channel(voice_channel)

    player = await voice.create_ytdl_player(url)
    player.start()


@client.event
async def on_message(message):
    if message.content.startswith("~yt"):
        args = message.content.split(" ")
        url = args[1]
        voice_channel = message.author.voice.voice_channel
        if voice_channel:
            await music_player(voice_channel, url)
        else:
            await client.send_message(message.channel, "You are not in a voice channel.")

client.run(token)
