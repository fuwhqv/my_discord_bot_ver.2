from discord.ext import commands
from baseball import Baseball


class minigames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = None

    @commands.command(name='play',
                      description='게임 진행을 위한 인풋/명령어 입력 커맨드',
                      aliases = ['input', 'move'])
    async def play(self, ctx, gCmd:str = None):
        if self.game is None:
            await ctx.send('No game playing!')
            return
        
        if gCmd is None:
            await ctx.send('Invalid input!')
            return

        result = self.game.update(gCmd)
        await ctx.send(result[1])

        if result[0] == 1:
            self.game = None
            
    @commands.command(name='숫자야구',
                      aliases=['baseball'])
    async def numberBaseball(self, ctx, digits:str ='3'):
        if self.game is not None:
            await ctx.send('A game is already on play!')
            return
        try:
            self.game = Baseball(int(digits))
            await ctx.send('The number is set, ready to play!')
        except:
            self.game = None
            await ctx.send('The number for digits is invalid!')


def setup(bot):
    bot.add_cog(minigames(bot))
