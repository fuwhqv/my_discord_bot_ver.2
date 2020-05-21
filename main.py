import discord
from discord.ext import commands
import os
import asyncio

ADMIN = int(os.environ['ADMIN_IDNUM'])
TOKEN = os.environ['BOT_TOKEN']
BOT_PREFIX = ('=', '$')
STARTUP_EXTENSIONS = ['chat', 'mornitor', 'emoji']

bot = commands.Bot(command_prefix = BOT_PREFIX)
ls = []

@bot.command(name="load"
                ,description="Load extension"
                ,pass_context=True)
async def load(ctx, extension_name : str=None):
    if ctx.message.author.id == ADMIN:
        if extension_name is not None:
            try:
                bot.load_extension(extension_name)
                ls.append(extension_name)
                await ctx.send("{} loaded.".format(extension_name))
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))
    else:
        #print(" "*45+"\033[93m^ Has no permission\033[0m")
        await ctx.send("ㅋ")
    
@bot.command(name="unload"
                ,description="Unload extension"
                ,pass_context=True)
async def unload(ctx, extension_name : str=None):
    if ctx.message.author.id == ADMIN:
        if extension_name is not None:
            try:
                bot.unload_extension(extension_name)
                ls.remove(extension_name)
                await ctx.send("{} unloaded.".format(extension_name))
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))
                await ctx.send("Failed to unload {}.".format(extension_name))
    else:
        #print(" "*45+"\033[93m^ Has no permission\033[0m")
        await ctx.send("ㅋ")

@bot.command(name="list"
                ,description="Shows available extensions"
                ,pass_context=True
                )
async def list(ctx):
    await ctx.send("List of extensions: {}".format(ls))


@bot.command(name="kill"
                ,description="봇을 강제로 종료. 발생하는 에러에 대해서는 책임 지지 않음."
                ,brief="I'll be back..."
                ,pass_context=True
                )
async def kill(ctx):
    if ctx.message.author.id == ADMIN:
        await ctx.send("전원을 종료합니다.")
        await bot.logout()
    else:
        #print(" "*45+"\033[93m^ Has no permission\033[0m")
        await ctx.send("ㅋ")


async def showStatus():
    await bot.wait_until_ready()
    os.system("cls")
    os.system("echo 로딩 완료!")
    itern=1
    await asyncio.sleep(1)
    while not bot.is_closed():
        os.system("cls")
        print("Logged in as " + bot.user.name)
        print("-"*45+"Current servers"+"-"*45)
        for server in bot.guilds:
            print("......"+server.name)
        print("-"*50+"{:^5}".format(itern)+"-"*50)
        itern+=1
        await asyncio.sleep(1800)


for extension in STARTUP_EXTENSIONS:
    try:
        bot.load_extension(extension)
        ls.append(extension)
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Failed to load extension {}\n{}'.format(extension, exc))


bot.loop.create_task(showStatus())
bot.run(TOKEN)
