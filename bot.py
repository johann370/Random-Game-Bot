import os
import discord
import random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='getgame')
async def get_game(ctx):
    with open('games.txt', 'r') as reader:
        games = []
        for line in reader:
            games.append(line)

    response = random.choice(games)
    await ctx.send(response, delete_after=5)


@bot.command(name='addgame')
async def add_game(ctx, game: str):
    with open('games.txt', 'r+') as file:
        if(game) not in file:
            file.write(f"\n{game}")
            await ctx.send(f"{game} was added to the list", delete_after=5)
        else:
            await ctx.send(f"{game} is already in the list", delete_after=5)


@bot.command(name='games')
async def get_games(ctx):
    with open('games.txt', 'r') as reader:
        games = []
        for line in reader:
            games.append(line.rstrip())

    message = ""
    for game in games:
        message += f"{game}\n"

    await ctx.send(message, delete_after=60)

bot.run(TOKEN)
