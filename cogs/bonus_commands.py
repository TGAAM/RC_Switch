import discord, random, os
from discord.ext import commands
import checks_list


def setup(bot):
        bot.add_cog(BonusCommands(bot))


class BonusCommands (commands.Cog):
    def __init__ (self, bot):
        self.bot = bot

# Other Commands
# beep, hi, home

    @commands.command()
    @commands.check(checks_list.is_valid_room)
    async def beep(self, ctx):
        await ctx.send("Boop!")
        return

    @commands.command(aliases=["hi", "howdy", "hey", "hola"])
    @commands.check(checks_list.is_valid_room)
    async def hello(self, ctx):
        responses = ("Hello", "Hi", "Howdy", "Hey", "Hola")
        choice = random.randint(0,len(responses)-1)
        await ctx.send(responses[choice])
        return
