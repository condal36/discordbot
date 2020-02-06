import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord.utils import get
from discord import FFmpegPCMAudio
import time
import youtube_dl


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
players = {}


bot = commands.Bot(command_prefix='=')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
@bot.command(pass_context=True, brief="This will show a daily cute pic", aliases=['dq'])
async def dailycute(ctx):

    await ctx.send(file=discord.File('./data/dailycute/1.jpg'))
@bot.command()
async def add(ctx, a:eval,b:eval):
    await ctx.send(a+b)
@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
@bot.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['pl'])
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music end or use the 'stop' command")
        return
    await ctx.send("Getting everything ready, playing audio soon")
    print("Someone wants to play music let me get that ready for them...")
    voice = get(bot.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, 'song.mp3')
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    voice.volume = 100
    voice.is_playing()
@bot.command()
async def play1(ctx):
    voice=get(bot.voice_clients,guild=ctx.guild)
    source = FFmpegPCMAudio('2.m4a')
    player = voice.play(source)
@bot.command()
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.pause()
@bot.command()
async def leave(ctx):
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    await voice_client.disconnent()
@bot.command(pass_context=True)
async def pt(ctx,url):
    voice=get(bot.voice_clients,guild=ctx.guild)
    source = FFmpegPCMAudio(url)
    player = voice.start(source)
@bot.command()
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.resume()
@bot.command()
async def multiply(ctx, a: eval, b: eval):
    await ctx.send(a*b)

@bot.command()
async def greet(ctx):
    await ctx.send(":smiley: :wave: Hello, there!")

@bot.command()
async def cat(ctx):
    await ctx.send("https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif")

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="島邊機器人", description="一個不起眼的島邊機器人", color=0xeee657)

    # give info about you here
    embed.add_field(name="Author", value="王蟲四竄北南")

    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    # give users a link to invite thsi bot to their server
    embed.add_field(name="Invite", value="[Invite link](DO NOT SUPPORT)")

    await ctx.send(embed=embed)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="nice bot", description="A Very Nice bot. List of commands are:", color=0xeee657)

    embed.add_field(name="=add X Y", value="Gives the addition of **X** and **Y**", inline=False)
    embed.add_field(name="=multiply X Y", value="Gives the multiplication of **X** and **Y**", inline=False)
    embed.add_field(name="=greet", value="Gives a nice greet message", inline=False)
    embed.add_field(name="=cat", value="Gives a cute cat gif to lighten up the mood.", inline=False)
    embed.add_field(name="=info", value="Gives a little info about the bot", inline=False)
    embed.add_field(name="=help", value="Gives this message", inline=False)
    embed.add_field(name="=dailycute", value="show a cute img of the day", inline=False)
    embed.add_field(name="=join", value="join current channel", inline=False)
    embed.add_field(name="=leave", value="leave current channel", inline=False)
    embed.add_field(name="=play", value="play [url](youtube)", inline=False)
    embed.add_field(name="=play1", value="play [url](youtube)", inline=False)

    await ctx.send(embed=embed)
bot.run(TOKEN)