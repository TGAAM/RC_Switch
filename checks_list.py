# Verification checks for commands

import discord
import os

# user roles
#playerRoles = [os.environ['RC_PLAYER_ROLES'].split(",")]

# channel whitelist
whitelistChannels = list(map(int,os.environ['RC_CHANNEL_WHITELIST'].split(",")))


# was the command from an active room?
async def is_valid_room(ctx):
    return (ctx.channel.id in whitelistChannels)

'''
# does the user have an eligible role to run commands?
async def is_player(ctx):
    # look through the list of player roles and check if the user has one
    for roleID in playerRoles:
        role = ctx.guild.get_role(roleID)
        if (role in ctx.author.roles):
            # only need one match to be valid
            return True
    
    # nothing found so not a player
    return False
'''