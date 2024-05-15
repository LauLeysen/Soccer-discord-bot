import os
import discord
import aiohttp
from discord.ext import commands
from discord.commands import slash_command
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the token from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')
API_BASE_URL = os.getenv('BASE_URI')  # Change this if your API is hosted elsewhere

description = 'Football Match Data Bot'

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.slash_command(description="Replies with Pong!")
async def ping(ctx):
    await ctx.respond('Pong!')

@bot.slash_command(description="Get all live matches")
async def live(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{API_BASE_URL}/live') as resp:
            if resp.status == 200:
                data = await resp.json()
                message = "\n".join([f"{match['home_team']} vs {match['away_team']}: {match['score']} ({match['time']})" for match in data])
                await ctx.respond(message if message else "No live matches found.")
            else:
                await ctx.respond("Failed to fetch live matches.")

@bot.slash_command(description="Get all upcoming matches")
async def upcoming(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{API_BASE_URL}/upcoming') as resp:
            if resp.status == 200:
                data = await resp.json()
                message = "\n".join([f"{match['home_team']} vs {match['away_team']}: {match['start_time']}" for match in data])
                await ctx.respond(message if message else "No upcoming matches found.")
            else:
                await ctx.respond("Failed to fetch upcoming matches.")

@bot.slash_command(description="Get all finished matches and results")
async def finished(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{API_BASE_URL}/finished') as resp:
            if resp.status == 200:
                data = await resp.json()
                message = "\n".join([f"{match['home_team']} {match['result']}" for match in data])
                await ctx.respond(message if message else "No finished matches found.")
            else:
                await ctx.respond("Failed to fetch finished matches.")

@bot.slash_command(description="Get live match details by team name")
async def match(ctx, team: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{API_BASE_URL}/match', params={'team': team}) as resp:
            if resp.status == 200:
                data = await resp.json()
                if data:
                    message = "\n".join([f"{match['home_team']} vs {match['away_team']}: {match['score']} ({match['time']})" for match in data])
                    await ctx.respond(message)
                else:
                    await ctx.respond(f"No live matches found for team: {team}")
            else:
                await ctx.respond(f"Failed to fetch live matches for team: {team}")

# Run the bot
bot.run(TOKEN)