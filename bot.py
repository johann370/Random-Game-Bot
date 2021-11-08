import os
import discord
import random
from discord.ext import commands
from dotenv import load_dotenv
import requests

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

steamids = {
    "JohannM": "76561198142616412",
    "MarcccOlives": "76561198404538375",
    "lightfriend7": "76561198236337610",
    "RedJasper": "76561198839766543",
    "Demon": "76561198167845439",
    "vegito523": "76561198142570382",
    "BOOMER": "76561199112017560"
}


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


@bot.command(name='getsteamgame')
async def get_steam_game(ctx):
    parameters = {
        "key": os.getenv('STEAM_KEY'),
        "steamid": steamids[ctx.message.author.name],
        "format": "json",
        "include_appinfo": True,
        "include_played_free_games": True
    }
    url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001"

    response = requests.get(url, params=parameters).json()['response']

    games = []

    for game in response['games']:
        games.append(game["name"])

    await ctx.send(random.choice(games), delete_after=10)


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
