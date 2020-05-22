from discord.ext import commands
import random

emojiGroups = {}

class emoji(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        await ctx.send('init0')
        for guild in self.bot.guilds:
            await ctx.send('init1.g{}'.format(guild.name))
            for em in guild.emojis:
                await ctx.send('init2.e{}'.format(em.name))
                emojiGroups[em.name] = (em.animated, em.id)


    @commands.command()
    async def ereload(self, ctx):
        emojiGroups = {}
        await ctx.send('erl0')
        for guild in self.bot.guilds:
            await ctx.send('erl1.g{}'.format(guild.name))
            for em in guild.emojis:
                await ctx.send('erl2.e{}'.format(em.name))
                emojiGroups[em.name] = (em.animated, em.id)
        '''for x in emojiGroups.items():
            print(x)'''


    @commands.command(name='emoji'
        ,description="이모지 출력"
        ,brief="이모지 출력"
        ,aliases=['e']
        )
    async def emoji(self, ctx, name:str = None):
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
        res = ''
        i=0
        await ctx.send('el0')
        for name, em in list(emojiGroups.items()):
            await ctx.send('el1.{}'.format(i))
            i+=1
            res += '<{0}:{1}:{2}> : `{1:15s}`{3}'\
                .format('a' if em[0] else '', name, em[1], '\n' if i%3 == 0 else ' ')
        await ctx.send('el2')
        await ctx.send(res)


def setup(bot):
    bot.add_cog(emoji(bot))