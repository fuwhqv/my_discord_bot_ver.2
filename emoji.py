from discord.ext import commands
import random

emojiGroups = None

class emoji(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        global emojiGroups
        emojiGroups = {}
        for guild in self.bot.guilds:
            for em in guild.emojis:
                emojiGroups[em.name] = (em.animated, em.id)


    @commands.command()
    async def ereload(self, ctx):
        global emojiGroups
        emojiGroups = {}
        for guild in self.bot.guilds:
            for em in guild.emojis:
                emojiGroups[em.name] = (em.animated, em.id)


    @commands.command(name='emoji'
        ,description="이모지 출력"
        ,brief="이모지 출력"
        ,aliases=['e']
        )
    async def emoji(self, ctx, name:str = None):
        global emojiGroups
        res = ''
        if name is None:
            tname, em = random.choice(list(emojiGroups.items()))
            res = '<{}:{}:{}>'.format('a' if em[0] else '', tname, em[1])
        else:
            em = emojiGroups.get(name)
            res = ':{}:'.format(name) if em is None else\
                  '<{}:{}:{}>'.format('a' if em[0] else '', name, em[1])
        await ctx.send(res)


    @commands.command()
    async def elist(self, ctx):
        global emojiGroups
        res = ''
        i=0
        for name, em in list(emojiGroups.items()):
            i+=1
            res += '<{0}:{1}:{2}> : `{1:15s}` '.format('a' if em[0] else '', name, em[1])
            if i%3==0:
                await ctx.send(res)
                res = ''
        await ctx.send(res)


def setup(bot):
    bot.add_cog(emoji(bot))