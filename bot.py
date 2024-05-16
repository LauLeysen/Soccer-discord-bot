import os
import discord
import aiohttp
from discord.ext import commands, tasks
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

# Global variables to keep track of the update channel and message
update_channel_id = None
live_message_id = None
previous_scores = {}
previous_statuses = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    update_live_scores.start()  # Start the task to update live scores periodically

@bot.command(description="Replies with Pong!")
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command(description="Remove multiple messages at ones")
async def purge(ctx, limit: str):
    """Deletes messages in the channel. Use 'all' to delete all messages."""
    if limit.lower() == 'all':
        deleted = await ctx.channel.purge()
        await ctx.send(f'Deleted {len(deleted)} messages.', delete_after=5)
    else:
        try:
            limit = int(limit)
            if limit < 1:
                await ctx.send('The limit must be greater than 0.')
                return
            deleted = await ctx.channel.purge(limit=limit)
            await ctx.send(f'Deleted {len(deleted)} messages.', delete_after=5)
        except ValueError:
            await ctx.send('Please provide a valid number of messages to delete or use "all".')

@bot.command(description="Get all live matches")
async def live(ctx):
    global update_channel_id, live_message_id
    update_channel_id = ctx.channel.id
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{API_BASE_URL}/live') as resp:
            if resp.status == 200:
                data = await resp.json()
                live_matches = []
                halftime_matches = []
                for match in data:
                    if match['status'] == "Live":
                        live_matches.append(f"**{match['home_team']} vs {match['away_team']}**\nScore: {match['score']} | Time: {match['time']}")
                    elif match['status'] == "Halftime":
                        halftime_matches.append(f"**{match['home_team']} vs {match['away_team']}**\nScore: {match['score']} (Halftime)")
                message = "\n\n".join(live_matches + halftime_matches) if live_matches or halftime_matches else "No live matches found."
            else:
                message = "Failed to fetch live matches."
            embed = discord.Embed(title="Live Matches", description=message, color=0x00ff00)
            msg = await ctx.send(embed=embed)
            live_message_id = msg.id

@bot.command(description="Get all upcoming matches")
async def upcoming(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{API_BASE_URL}/upcoming') as resp:
            if resp.status == 200:
                data = await resp.json()
                message = "\n\n".join([f"**{match['home_team']} vs {match['away_team']}**\n {match['status']}" for match in data])
                embed = discord.Embed(title="Upcoming Matches", description=message, color=0x0000ff)
                await ctx.send(embed=embed if message else "No upcoming matches found.")
            else:
                await ctx.send("Failed to fetch upcoming matches.")

@bot.command(description="Get all finished matches and results")
async def finished(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{API_BASE_URL}/finished') as resp:
            if resp.status == 200:
                data = await resp.json()
                message = "\n\n".join([f"**{match['home_team']}** {match['result']}" for match in data])
                embed = discord.Embed(title="Finished Matches", description=message, color=0xff0000)
                await ctx.send(embed=embed if message else "No finished matches found.")
            else:
                await ctx.send("Failed to fetch finished matches.")

@bot.command(description="Get live match details by team name")
async def match(ctx, team: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{API_BASE_URL}/match', params={'team': team}) as resp:
            if resp.status == 200:
                data = await resp.json()
                if data:
                    message = "\n\n".join([f"**{match['home_team']} vs {match['away_team']}**\nScore: {match['score']} | Time: {match['time']}" for match in data])
                    embed = discord.Embed(title=f"Live Matches for {team}", description=message, color=0x00ff00)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"No live matches found for team: {team}")
            else:
                await ctx.send(f"Failed to fetch live matches for team: {team}")

@bot.command(description="Start updating live match scores in this channel")
async def start_updates(ctx):
    global update_channel_id, live_message_id
    update_channel_id = ctx.channel.id
    async with ctx.channel.typing():
        msg = await ctx.send("Starting live match updates...")
        live_message_id = msg.id
    await ctx.send("Live match updates started!")

@tasks.loop(seconds=10)
async def update_live_scores():
    global live_message_id, previous_scores, previous_statuses
    if update_channel_id is None:
        return
    channel = bot.get_channel(update_channel_id)
    if channel is None:
        return
    role = discord.utils.get(channel.guild.roles, name="pinglive")
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{API_BASE_URL}/live') as resp:
            if resp.status == 200:
                data = await resp.json()
                live_matches = []
                halftime_matches = []
                for match in data:
                    match_key = f"{match['home_team']} vs {match['away_team']}"
                    current_score = match['score']
                    current_status = match['status']
                    if current_status == "Live":
                        live_matches.append(f"**{match['home_team']} vs {match['away_team']}**\nScore: {current_score} | Time: {match['time']}")
                    elif current_status == "Halftime":
                        halftime_matches.append(f"**{match['home_team']} vs {match['away_team']}**\nScore: {current_score} (Halftime)")

                    # Check for score change and ping the role
                    if match_key in previous_scores and previous_scores[match_key] != current_score:
                        await channel.send(f"{role.mention} {match['home_team']} vs {match['away_team']} score changed: {previous_scores[match_key]} -> {current_score}")
                    
                    # Check for match end and ping the role
                    if match_key in previous_statuses and previous_statuses[match_key] in ["Live", "Halftime"] and current_status == "Finished":
                        await channel.send(f"{role.mention} {match['home_team']} vs {match['away_team']} has ended with a score of {current_score}")

                    previous_scores[match_key] = current_score
                    previous_statuses[match_key] = current_status

                message = "\n\n".join(live_matches + halftime_matches) if live_matches or halftime_matches else "No live matches found."
                embed = discord.Embed(title="Live Matches", description=message, color=0x00ff00)
            else:
                embed = discord.Embed(title="Error", description="Failed to fetch live matches.", color=0xff0000)

        try:
            msg = await channel.fetch_message(live_message_id)
            await msg.edit(embed=embed)
        except discord.NotFound:
            msg = await channel.send(embed=embed)
            live_message_id = msg.id

# Run the bot
bot.run(TOKEN)