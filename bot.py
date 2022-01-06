# -----------------------------------------------------------------------------------------------
# Switch Remote Control Discord bot for use with Sys-botbase
# -----------------------------------------------------------------------------------------------

# Switch Commands
# DU (DUP), DR (DRIGHT), DL (DLEFT), DD (DDOWN), A, B, X, Y, L, R, ZL, ZR, CAP (CAPTURE, PICTURE), PLUS, MINUS
# LS (LEFTSTICK) <DIRECTION> <DURATION>, RS (RIGHTSTICK) <DIRECTION> <DURATION>

# Other Commands
# beep, hi, home



from asyncio import tasks
from discord.ext import tasks
from typing import Match
from asyncio.tasks import sleep, wait, wait_for
import discord, os, random, asyncio, traceback, threading
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.ext.commands import CheckFailure
from discord.ext.commands import MissingRequiredArgument

# Discord bot token 
botToken = os.environ["RC_TOKEN"]

# setup a discord client
bot = commands.Bot(command_prefix=".", case_insensitive=True, description="Remote control bot")

# Switch IP
ipAddress = os.environ["RC_IP"]

# command processing lock
commandLock = threading.Lock()
commandWaiting = False

# commands
waitingCommand = []
activeCommand = []

# repeating max
REPT_MAX_BTN = 5
REPT_MAX_STICK = 5

# don't work in DMs
@bot.check
async def globally_block_dms(ctx):
    return ctx.guild is not None


# initial setup 
@bot.event
async def on_ready():
    cogs = ["cogs.bonus_commands"]
    for cog in cogs:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print("Problem with loading: " + str(cog))
            traceback.print_exc()

    # notify the log that it's ready
    print('We have logged in as {0.user}'.format(bot))

    # start the input loop
    inputLoop.start()


# error handling
@bot.event
async def on_command_error(ctx, error):
    # ignore errors that are invalid commands or calls from failed checks for now
    if isinstance(error, CheckFailure):
        #await ctx.send("checkFailure")
        print ("room check failure")
        return
    elif isinstance(error, CommandNotFound):
        if (await checks_list.is_valid_room(ctx)):
            await ctx.message.add_reaction("❌")
            await ctx.message.reply("That's not a valid command")
        return
    elif isinstance(error, MissingRequiredArgument):
        if (await checks_list.is_valid_room(ctx)):
            await ctx.message.add_reaction("❌")
            await ctx.message.reply("You need to include more details for this command")
        return
    raise error

import discord, random, os, socket, time
from discord.ext import commands
import checks_list

def is_cnt_error (cnt):
    try:
        assert int(cnt) == float(cnt)
    except:
        return True
    return False
    
def cnt_out_of_range (cnt, min, max):
    try:
        assert cnt >= min
        assert cnt <= max
    except:
        return True
    return False

# input loop
@tasks.loop(seconds=0.1)
async def inputLoop():
    global commandWaiting, activeCommand, waitingCommand
    commandLock.acquire()
    if (commandWaiting):
        activeCommand = waitingCommand
        waitingCommand = []
        commandWaiting = False
        await process_input(activeCommand)
    commandLock.release()
    return


# ready commands
async def process_command(ctx, cnt, cntMax, inputType, inputArray):
    global commandWaiting, waitingCommand
    if cnt is None:
        cnt = 1
    if is_cnt_error(cnt):
        await ctx.message.add_reaction("❌")
        await ctx.message.reply("There's an issue with the count")
        return
    cnt = int(cnt)
    if cnt_out_of_range(cnt, 1, cntMax):
        await ctx.message.add_reaction("❌")
        await ctx.message.reply("Count out of range")
        return
    if (not commandWaiting):
        commandWaiting = True
    waitingCommand = [inputType, ctx, cnt] + inputArray
    await ctx.message.add_reaction('✅')
    return

# handle button inputs
async def button_input(ctx, input, cnt=1):
    for i in range(cnt):
        sendCommand(s, input)
        await asyncio.sleep(1)
    print(input)
    return


# handle stick inputs, noticeably different logic from buttons
async def stick_input(ctx, stick, dir, cnt=1):
    sendCommand(s, "setStick " + stick + " " + dir)
    await asyncio.sleep(cnt)
    sendCommand(s, "setStick " + stick + " 0 0")
    print(stick + " " + dir)
    return

# hold down the buttons
def press(pressList=None):
    for btn in pressList:
        sendCommand(s, "press " + btn)
    return

# release held buttons
def release(pressList=None):
    for btn in pressList:
        sendCommand(s, "release " + btn)
    return

# process the current input command
async def process_input(commandString):
    if (commandString[0] == "button"):
        await button_input(commandString[1], commandString[3], commandString[2])
    else:
        await stick_input(commandString[1],commandString[3],commandString[4],commandString[2])
    return


# commands
@bot.command()
@commands.check(checks_list.is_valid_room)
async def home(ctx):
	await ctx.message.reply("<a:youTried:811011120172761100>")
	return

@bot.command(aliases=["cap", "picture", "screenshot", "snapshot", "photo"])
@commands.check(checks_list.is_valid_room)
async def capture(ctx, cnt=None):
    await process_command(ctx, 1, 1, "button", ["click Capture"])
    return

@bot.command(aliases=["ru", "runUp"])
@commands.check(checks_list.is_valid_room)
async def rup(ctx, cnt=None):
    await process_command(ctx, cnt, REPT_MAX_STICK, "stick", ["LEFT", "0 0x7FFF"])
    return

@bot.command(aliases=["rd", "runDown"])
@commands.check(checks_list.is_valid_room)
async def rdown(ctx, cnt=None):
    await process_command(ctx, cnt, REPT_MAX_STICK, "stick", ["LEFT", "0 -0x8000"])
    return

@bot.command(aliases=["rl", "runLeft"])
@commands.check(checks_list.is_valid_room)
async def rleft(ctx, cnt=None):
    await process_command(ctx, cnt, REPT_MAX_STICK, "stick", ["LEFT", "-0x8000 0"])
    return

@bot.command(aliases=["rr", "runRight"])
@commands.check(checks_list.is_valid_room)
async def rright(ctx, cnt=None):
    await process_command(ctx, cnt, REPT_MAX_STICK, "stick", ["LEFT", "0x7FFF 0"])
    return

@bot.command(aliases=["du", "up"])
@commands.check(checks_list.is_valid_room)
async def dup(ctx, cnt=None):
    await process_command(ctx, cnt, REPT_MAX_BTN, "button", ["click DUP"])
    return


@bot.command(aliases=["dd", "down"])
@commands.check(checks_list.is_valid_room)
async def ddown(ctx, cnt=None):
    await process_command(ctx, cnt, REPT_MAX_BTN, "button", ["click DDOWN"])
    return

@bot.command(aliases=["dl", "left"])
@commands.check(checks_list.is_valid_room)
async def dleft(ctx, cnt=None):
    await process_command(ctx, cnt, REPT_MAX_BTN, "button", ["click DLEFT"])
    return

@bot.command(aliases=["dr", "right"])
@commands.check(checks_list.is_valid_room)
async def dright(ctx, cnt=None):
    await process_command(ctx, cnt, REPT_MAX_BTN, "button", ["click DRIGHT"])
    return

@bot.command()
@commands.check(checks_list.is_valid_room)
async def a(ctx, cnt=None):
    await process_command(ctx, cnt, REPT_MAX_BTN, "button", ["click A"])
    return

@bot.command()
@commands.check(checks_list.is_valid_room)
async def b(ctx, cnt=None):
    await process_command(ctx, cnt, REPT_MAX_BTN, "button", ["click B"])
    return

@bot.command()
@commands.check(checks_list.is_valid_room)
async def x(ctx, cnt=None):
    await process_command(ctx, cnt, REPT_MAX_BTN, "button", ["click X"])
    return

@bot.command()
@commands.check(checks_list.is_valid_room)
async def y(ctx, cnt=None):
    await process_command(ctx, cnt, REPT_MAX_BTN, "button", ["click Y"])
    return

@bot.command()
@commands.check(checks_list.is_valid_room)
async def l(ctx, cnt=None):
    await process_command(ctx, cnt, REPT_MAX_BTN, "button", ["click L"])
    return

@bot.command()
@commands.check(checks_list.is_valid_room)
async def r(ctx, cnt=None):
    await process_command(ctx, cnt, REPT_MAX_BTN, "button", ["click R"])
    return

@bot.command()
@commands.check(checks_list.is_valid_room)
async def zl(ctx, cnt=None):
    await process_command(ctx, cnt, REPT_MAX_BTN, "button", ["click ZL"])
    return

@bot.command()
@commands.check(checks_list.is_valid_room)
async def zr(ctx, cnt=None):
    await process_command(ctx, cnt, REPT_MAX_BTN, "button", ["click ZR"])
    return

@bot.command(aliases=["start", "+"])
@commands.check(checks_list.is_valid_room)
async def plus(ctx, cnt=None):
    await process_command(ctx, cnt, REPT_MAX_BTN, "button", ["click PLUS"])
    return

@bot.command(aliases=["select", "-"])
@commands.check(checks_list.is_valid_room)
async def minus(ctx, cnt=None):
    await process_command(ctx, cnt, REPT_MAX_BTN, "button", ["click MINUS"])
    return


# connect to switch
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ipAddress, 6000))

def sendCommand(s, command):
    command += '\r\n'
    s.sendall(command.encode())

# start the program
bot.run(botToken)
