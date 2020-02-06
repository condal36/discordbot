import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import youtube_dl
Client = discord.Client()
bot = commands.Bot(command_prefix = ",")
@bot.command(pass_context=True)
async def play(ctx):
    voice = await bot.join_voice_channel(ctx.message.author.voice.voice_channel)
    args = ctx.message.content.split(" ")
    betterargs = " ".join(args[1:])
    player = await voice.create_ytdl_player('https://www.youtube.com/watch?v=' + betterargs)
    player.start()

@bot.command(pass_context=True)
async def leavevoice(ctx):
    for x in bot.voice_clients:
        if(x.server == ctx.message.server):
            return await x.disconnect()