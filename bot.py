import os
import discord
from discord.ext import commands
from discord.commands import slash_command
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the token from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')
ADMIN_ROLE_NAME = "pinglive"  # Change this to your Admin role name

description = 'test bot'

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

# Run the bot
bot.run(TOKEN)
