# -----------------------------------------------------------------------------------------------
# Switch Remote Control Discord bot for use with Sys-botbase
# -----------------------------------------------------------------------------------------------

# Switch Commands
# DU (DUP), DR (DRIGHT), DL (DLEFT), DD (DDOWN), A, B, X, Y, L, R, ZL, ZR, CAP (CAPTURE, PICTURE), PLUS, MINUS
# LS (LEFTSTICK) <DIRECTION> <DURATION>, RS (RIGHTSTICK) <DIRECTION> <DURATION>

# Other Commands
# beep, hi, home

# import modules
# For hosting from Heroku/Github I had to include a Requirements.txt file with the following
'''
discord.py==1.3.3
psycopg2==2.8.5
'''

import discord
import os
import random
import asyncio
import traceback
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.ext.commands import CheckFailure
from discord.ext.commands import MissingRequiredArgument

# Discord bot token 
botToken = os.environ['RC_TOKEN']

# setup a discord client
bot = commands.Bot(command_prefix=".", case_insensitive=True, description="Remote control bot")


# don't work in DMs
@bot.check
async def globally_block_dms(ctx):
    return ctx.guild is not None

async def is_valid_room(ctx):
    return (ctx.channel.id in whitelistChannels)

async def is_user(ctx):
    # look through the list of bot user roles and check if the requestor has one
    for roleID in userRoles:
        role = ctx.guild.get_role(roleID)
        if (role in ctx.author.roles):
            # only need one match to be valid
            return True
    
    # nothing found so not a bot user
    return False

# initial setup 
@bot.event
async def on_ready():
    cogs = ["cogs.remote_control"]
    for cog in cogs:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print("Problem with loading: " + str(cog))
            traceback.print_exc()

    # notify the log that it's ready
    print('We have logged in as {0.user}'.format(bot))


# error handling
@bot.event
async def on_command_error(ctx, error):
    # ignore errors that are invalid commands or calls from failed checks for now
    if isinstance(error, CommandNotFound):
        return
    elif isinstance(error, CheckFailure):
        return
    elif isinstance(error, MissingRequiredArgument):
        await ctx.send("You need to include more details for this command")
        return

    raise error

# start the program
bot.run(botToken)
