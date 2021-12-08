import discord, random
from discord.ext import commands
import checks_list


def setup(bot):
        bot.add_cog(RemoteControl(bot))


class RemoteControl (commands.Cog):
    def __init__ (self, bot):
        self.bot = bot

# Switch Commands
# DU (DUP), DR (DRIGHT), DL (DLEFT), DD (DDOWN), A, B, X, Y, L, R, ZL, ZR, CAP (CAPTURE, PICTURE), PLUS, MINUS
# LS (LEFTSTICK) <DIRECTION> <DURATION>, RS (RIGHTSTICK) <DIRECTION> <DURATION>

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

    @commands.command()
    @commands.check(checks_list.is_valid_room)
    async def home(self, ctx):
        await ctx.send("no")
        return


    @commands.command(aliases=["du"])
    @commands.check(checks_list.is_valid_room)
    async def dup(self, ctx):
        await ctx.send("d up")
        return

    @commands.command(aliases=["dd"])
    @commands.check(checks_list.is_valid_room)
    async def ddown(self, ctx):
        await ctx.send("d down")
        return

    @commands.command(aliases=["dl"])
    @commands.check(checks_list.is_valid_room)
    async def dleft(self, ctx):
        await ctx.send("d left")
        return

    @commands.command(aliases=["dr"])
    @commands.check(checks_list.is_valid_room)
    async def dright(self, ctx):
        await ctx.send("d right")
        return

    @commands.command()
    @commands.check(checks_list.is_valid_room)
    async def a(self, ctx):
        await ctx.send("A")
        return

    @commands.command()
    @commands.check(checks_list.is_valid_room)
    async def b(self, ctx):
        await ctx.send("B")
        return

    @commands.command()
    @commands.check(checks_list.is_valid_room)
    async def x(self, ctx):
        await ctx.send("X")
        return

    @commands.command()
    @commands.check(checks_list.is_valid_room)
    async def y(self, ctx):
        await ctx.send("Y")
        return

    @commands.command()
    @commands.check(checks_list.is_valid_room)
    async def l(self, ctx):
        await ctx.send("L")
        return

    @commands.command()
    @commands.check(checks_list.is_valid_room)
    async def r(self, ctx):
        await ctx.send("R")
        return

    @commands.command()
    @commands.check(checks_list.is_valid_room)
    async def zl(self, ctx):
        await ctx.send("ZL")
        return

    @commands.command()
    @commands.check(checks_list.is_valid_room)
    async def zr(self, ctx):
        await ctx.send("ZR")
        return

    @commands.command(aliases=["start", "+"])
    @commands.check(checks_list.is_valid_room)
    async def plus(self, ctx):
        await ctx.send("plus")
        return

    @commands.command(aliases=["select", "-"])
    @commands.check(checks_list.is_valid_room)
    async def minus(self, ctx):
        await ctx.send("minus")
        return

    @commands.command(aliases=["cap", "picture", "screenshot", "snapshot", "photo"])
    @commands.check(checks_list.is_valid_room)
    async def capture(self, ctx):
        await ctx.send("capture")
        return

    @commands.command(aliases=["lstick", "lefts", "ls"])
    @commands.check(checks_list.is_valid_room)
    async def leftstick(self, ctx, direction, duration):
        try:
            assert int(direction) == float(direction)
            direction = int(direction)
            assert direction >= 1
            assert direction <=12
            
        except:
            await ctx.send("Unable to resolve direction: " + str(direction))
            return

        try:
            assert int(duration) == float(duration)
            duration = int(duration)
            assert duration >= 1
            assert duration <=10
            
        except:
            await ctx.send("Unable to resolve duration: " + str(duration))
            return

        await ctx.send("Left stick: " + str(direction) + ", " + str(duration))
        return

    @commands.command(aliases=["rstick", "rights", "rs"])
    @commands.check(checks_list.is_valid_room)
    async def rightstick(self, ctx, direction, duration):
        try:
            assert int(direction) == float(direction)
            direction = int(direction)
            assert direction >= 1
            assert direction <=12
            
        except:
            await ctx.send("Unable to resolve direction: " + str(direction))
            return

        try:
            assert int(duration) == float(duration)
            duration = int(duration)
            assert duration >= 1
            assert duration <=10
            
        except:
            await ctx.send("Unable to resolve duration: " + str(duration))
            return

        await ctx.send("Right stick: " + str(direction) + ", " + str(duration))
        return

