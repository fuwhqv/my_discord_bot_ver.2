from discord.ext import commands
from baseball import Baseball
from wordle import Wordle

class minigames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = {}

    @commands.command(description='게임 진행을 위한 인풋/명령어 입력 커맨드',
                      aliases = ['input', 'move'])
    async def play(self, ctx, gCmd:str = None):
        gGame = self.game.get(ctx.guild)
        if gGame is None:
            await ctx.send('No game playing!')
            return
        
        if gCmd is None:
            await ctx.send('Invalid input!')
            return

        result = gGame.update(gCmd)
        for res in result[1:]:
            await ctx.send(res)

        if result[0] == 1:
            self.game[ctx.guild] = None
            
    @commands.command(description='숫자야구(3~4자리)',
                      aliases=['baseball'])
    async def numberBaseball(self, ctx, digits:str ='3'):
        if self.game.get(ctx.guild) is not None:
            await ctx.send('A game is already on play!')
            return
        try:
            self.game[ctx.guild] = Baseball(int(digits))
            await ctx.send('The number is set, ready to play!')
        except:
            self.game[ctx.guild] = None
            await ctx.send('The number for digits is invalid!')

    @commands.command(description='워들')
    async def wordle(self, ctx, hard:str = 'Normal'):
        if self.game.get(ctx.guild) is not None:
            await ctx.send('A game is already on play!')
            return
        try:
            self.game[ctx.guild] = Wordle(hard.upper() == 'HARD')
            await ctx.send('The word is chosen, ready to play!')
        except:
            self.game[ctx.guild] = None
            await ctx.send('Failed to create a wordle game...')


def setup(bot):
    bot.add_cog(minigames(bot))
