from discord.ext import commands
from baseball import Baseball


class minigames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = None

    @commands.command(name='게임 진행',
                      description='게임 진행을 위한 인풋/명령어 입력 커맨드')
    async def play(self, ctx, gCmd):
        if gCmd is None:
            await ctx.send('Invalid input!')
            return

        result = self.game.update(gCmd)
        await ctx.send(result[1])

        if result[0] == 1:
            self.game = None

    @commands.command(name='숫자야구',
                      aliases=['baseball'])
    async def numberBaseball(self, digits='3'):
        if self.game is not None:
            await ctx.send('A game is already on play!')
            return
        try:
            self.game = Baseball(int(digits))
        except:
            self.game = None
            await ctx.send('The number for digits is invalid!')


def setup(bot):
    bot.add_cog(minigames(bot))