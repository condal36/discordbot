import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord.utils import get
from discord import FFmpegPCMAudio


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')



bot = commands.Bot(command_prefix='=')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

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
    source = FFmpegPCMAudio('1.m4a')
    while True:
        player = voice.play(source)
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
    embed = discord.Embed(title="nice bot", description="Nicest bot there is ever.", color=0xeee657)

    # give info about you here
    embed.add_field(name="Author", value="<YOUR-USERNAME>")

    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    # give users a link to invite thsi bot to their server
    embed.add_field(name="Invite", value="[Invite link](<insert your OAuth invitation link here>)")

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

    await ctx.send(embed=embed)

bot.run(TOKEN)