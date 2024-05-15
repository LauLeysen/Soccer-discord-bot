import discord
from discord.ext import commands
from discord.commands import slash_command
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the token from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')

# Initialize the bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)
try:
    # Define a slash command
    @bot.slash_command(description="Replies with Pong!")
    async def ping(ctx):
        await ctx.respond('Pong!')
except Exception as e:
    print(e)
# Event to show when the bot is ready and working
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

# Run the bot
bot.run(TOKEN)

