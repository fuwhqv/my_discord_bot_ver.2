########## This is used for printing colored output ##########
import ctypes
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
##############################################################

import re
import os
import unicodedata
from discord.ext import commands
from discord.ext.commands import CheckFailure

################# Dataset for mornitoring ####################
server_ids_bwords=frozenset([
                            "523879052046761993"#BotCoding
                            ])
##############################################################

############ functions for formatting strings ################
def preformat_cjk (string, width, align='<', fill=' '):
    count = (width - sum(1 + (unicodedata.east_asian_width(c) in "WF")
                         for c in string))
    return {
        '>': lambda s: fill*count+s,
        '<': lambda s: s+fill*count,
        '^': lambda s: fill*(int)((count-count%2)/2)+s+fill*(int)((count+count%2)/2)
    }[align](string)

symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
           u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")
tr = {ord(a):ord(b) for a, b in zip(*symbols)}

def has_cyrillic(text):
    return bool(re.search('[\u0400-\u04FF]', text))

def myformat(str,len,align='<'):
    return preformat_cjk(str.translate(tr) if has_cyrillic(str) else str,len,align)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def serverstr(str,len,align='<'):
    return bcolors.OKBLUE+"["+bcolors.ENDC+"{}".format(myformat(str,11,align))+bcolors.OKBLUE+"]"
##############################################################

################### functions for printing ###################
def printcomm(message,BOT_PREFIX):
    if message.content[0] in BOT_PREFIX:
        print(
            serverstr(message.author.guild.name,11,align='^')+
            bcolors.HEADER+"[command]"+
            bcolors.ENDC+"{}: {}".
            format(myformat(message.author.name,20)
                    ,message.content
                    ))

def printinfo(message):
    print(
        serverstr(message.author.guild.name,11,align='^')+
        bcolors.WARNING+"[others ]"+
        bcolors.ENDC+"{}: img/clip".format(myformat(message.author.name,20)))
##############################################################

########################## bot class #########################
class Mornitor(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.printer=False
        with open("blist.txt",mode="r",encoding="utf-8") as file:
            self.blist = [b_word.strip().lower() for b_word in file.readlines()]

    @commands.Cog.listener()
    async def on_member_update(self,before,after):
        if not self.printer: return
        if before.activity!=after.activity:
            print(
                serverstr(before.guild.name,11,align='^')+
                bcolors.OKGREEN+"[status ]"+
                bcolors.ENDC+"{}:{}=>{}".
                format(myformat(before.name,20)
                    ,myformat(before.activity.name if before.activity else "",30,align='^')
                    ,myformat(after.activity.name if after.activity else "",30,align='^')
                    ))
        if before.status!=after.status:
            print(
                serverstr(before.guild.name,11,align='^')+
                bcolors.OKGREEN+"[status ]"+
                bcolors.ENDC+"{}:{}=>{}".
                format(myformat(before.name,20)
                    ,myformat(str(before.status),30,align='^')
                    ,myformat(str(after.status),30,align='^')
                    ))


    @commands.Cog.listener()
    async def on_message(self,message):
        for bad_word in self.blist:
            if bad_word in message.content.lower():
                await message.delete()
                if self.printer:
                    print(
                        serverstr(message.author.guild.name,11,align='^')+
                        bcolors.FAIL+"[deleted]"+
                        bcolors.ENDC+"{}: {}".
                        format(myformat(message.author.name,20)
                                ,message.content
                                ))

        if not self.printer: return
        try:
            printcomm(message,self.bot.command_prefix)
        except:
            printinfo(message)
        if message.author==self.bot.user:
            print(
                serverstr(message.author.guild.name,11,align='^')+
                bcolors.HEADER+"[ react ]"+
                bcolors.ENDC+"{}: {}".
                format(myformat(str(message.author.name),20)
                    ,message.content
            ))

    @commands.Cog.listener()
    async def on_command_error(self,error,context):
        if not self.printer: return
        print(" "*45+bcolors.WARNING+"^ No such command"+bcolors.ENDC)


    @commands.command()
    async def consoleTrigger(self, ctx):
        self.printer = not self.printer

def setup(bot):
    bot.add_cog(Mornitor(bot))