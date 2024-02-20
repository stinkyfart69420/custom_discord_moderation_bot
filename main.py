import discord
import os
import requests
import asyncio
import sqlite3
from discord.ext import commands
from discord.ext.commands import Bot


bot = commands.Bot(command_prefix='-', intents = discord.Intents.all())
DATABASE_FILE = "warnings.db"
conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS warnings (
        user_id INTEGER,
        moderator_id INTEGER,
        reason TEXT
    )
''')
conn.commit()


queues = {}


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="Try running -commands"))


    
@bot.command(name='warn', help='Warns a member. ||Usage: -warn @user reason||')
async def warn(ctx, user: discord.Member, *, reason: str):
    if ctx.author.guild_permissions.administrator:
        cursor.execute('''
            INSERT INTO warnings (user_id, moderator_id, reason)
            VALUES (?, ?, ?)
        ''', (user.id, ctx.author.id, reason))
        conn.commit()

        await ctx.send(f'{user.mention} has been warned for: {reason}')
    else:
        await ctx.send('You do not have permission to use this command.')



@bot.command(name='warnings', help='Check for warnings for a specified member. ||Usage: -warnings @user||')
async def view_warnings(ctx, user: discord.Member):
    if ctx.author.guild_permissions.administrator:
        cursor.execute('''
            SELECT moderator_id, reason
            FROM warnings
            WHERE user_id = ?
        ''', (user.id,))
        warnings = cursor.fetchall()

        if warnings:
            warning_list = '\n'.join([f'Moderator: {bot.get_user(w[0])}, Reason: {w[1]}' for w in warnings])
            await ctx.send(f'Warnings for {user.mention}:\n{warning_list}')
        else:
            await ctx.send(f'{user.mention} has no warnings.')

@bot.command(name='unwarn', help='Unwarns a member ||Usage: -unwarn @user number of warnings to be removed||')
async def unwarn(ctx, user: discord.Member, warning_number: int):
    if ctx.author.guild_permissions.administrator:
        cursor.execute('''
            SELECT moderator_id, reason
            FROM warnings
            WHERE user_id = ?
        ''', (user.id,))
        warnings = cursor.fetchall()

        if warnings and 0 < warning_number <= len(warnings):
            moderator_id, reason = warnings[warning_number - 1]
            cursor.execute('''
                DELETE FROM warnings
                WHERE user_id = ? AND moderator_id = ? AND reason = ?
            ''', (user.id, moderator_id, reason))
            conn.commit()

            await ctx.send(f'Removed warning {warning_number} for {user.mention}: Moderator: {bot.get_user(moderator_id)}, Reason: {reason}')
        else:
            await ctx.send(f'Invalid warning number or {user.mention} has no warnings.')
    else:
        await ctx.send('You do not have permission to use this command.')



@bot.command(name="kick",help='Kicks a member. ||Usage: -kick @user reason||')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)

    try:
        await member.send(f"You have been kicked from the server by *{ctx.author.display_name}*. Reason: {reason}")
    except discord.Forbidden:
        await ctx.send("Member has been kicked.")

    await ctx.send(f"{member.display_name} has been kicked by {ctx.author.display_name}. Reason: {reason}")




@bot.command(name='weather', help='Check the weather! ||Usage: -weather country||')
async def weather(ctx, city):
    api_key = "Bj8Y71RfD2gZcoofYb8WxEBdsUPPFdkM"
    base_url = 'http://dataservice.accuweather.com/locations/v1/cities/search'
    
    params = {
        'apikey': api_key,
        'q': city,
        'details': 'false', 
    }

    try:
        response = requests.get(base_url, params=params)
        location_data = response.json()

        if not location_data:
            await ctx.send(f"Couldn't find information for {city}.")
            return

        location_key = location_data[0]['Key']

        weather_url = f'http://dataservice.accuweather.com/currentconditions/v1/{location_key}'
        params = {'apikey': api_key}
        weather_response = requests.get(weather_url, params=params)
        weather_data = weather_response.json()[0]

        temperature = weather_data['Temperature']['Metric']['Value']
        weather_text = weather_data['WeatherText']

        await ctx.send(f'The current weather in {city} is {weather_text} with a temperature of {temperature}°C.')
    except Exception as e:
        print(e)
        await ctx.send(f"Couldn't retrieve weather information for {city}.")

      
@bot.command(name='ban', help='Bans a specified member. ||Usage: -ban @user reason||')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
   
    try:
        await member.send(f"You have been banned from the server by *{ctx.author.display_name}*. Reason: {reason}")
    except discord.Forbidden:
        await ctx.send("Member has been banned.")

    await ctx.send(f"{member.display_name} has been banned by *{ctx.author.display_name}*. Reason: {reason}")




@bot.command(name='mute', help='Mutes a member. ||Usage: -mute @user||')
async def mute(ctx, member: discord.Member):
    
    if ctx.author.guild_permissions.manage_roles:
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False)
        
        await member.add_roles(muted_role)
        await ctx.send(f'{member.mention} has been muted.')
    else:
        await ctx.send("You do not have the necessary permissions to use this command.", delete_after=5)

@bot.command(name='unmute', help='Unmutes a member. ||Usage: -unmute @user||')
async def unmute(ctx, member: discord.Member):
    
    if ctx.author.guild_permissions.manage_roles:
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False)
        
        await member.remove_roles(muted_role)
        await ctx.send(f'{member.mention} has been unmuted.')
    else:
        await ctx.send("You do not have the necessary permissions to use this command.", delete_after=5)





        


@bot.command(name='purge', help='Purges the specified amount of messages ||Usage: -purge 5||')
async def purge(ctx, limit: int):
    if ctx.message.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=limit + 1)
        await ctx.send(f'{limit} messages purged.', delete_after=5)
    else:
        await ctx.send("You don't have permission to do that.", delete_after=5)


    
@bot.command(name='ping', help='Pong!')
async def ping(ctx):
    latency = round(bot.latency * 1000) 
    await ctx.send(f'Pong! Latency: {latency}ms')

@bot.command()
async def commands(ctx):
    """Show a list of available commands."""
    embed = discord.Embed(title="Command List", description="List of available commands:")
    for command in bot.commands:
        embed.add_field(name=command.name, value=command.help, inline=False)

    await ctx.send(embed=embed)


bot.run("BOT_TOKEN")

