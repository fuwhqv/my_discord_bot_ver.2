from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure

class chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def ping(self, ctx, n:int = 1):
        for _ in range(n):
            await ctx.send("Pong!")


    @commands.command(name='clear'
        ,description="최대 100개의 채팅 로그 삭제"
        ,pass_context=True
        )
    @has_permissions(manage_messages=True)
    async def clear(self,ctx,num:int = 1):
        mgs=[]
        num=int(num)
        if num>100:
            num=100
        if num<1:
            num=1
        await ctx.channel.purge(limit = num)
    @clear.error
    async def clear_error(self,error,ctx):
        if isinstance(error,CheckFailure):
            print(" "*45+bcolors.WARNING+"^ Has no permission"+bcolors.ENDC)


def setup(bot):
    bot.add_cog(chat(bot))
