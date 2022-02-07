from discord.ext import commands
from baseball    import Baseball
from wordle      import Wordle

emojiToColor = {
    '⬛': 'Black',
    '🟨': 'Yellow',
    '🟩': 'Green'
}

class minigames(commands.Cog):
    def __init__(self, bot):
        self.bot  = bot
        self.game = {}
        self.isEmojiLoaded = False
        self.emojiGroups = {}


    def loadEmojis(self):
        if self.isEmojiLoaded: return
        self.emojiGroups = {}
        for guild in self.bot.guilds:
            if guild.id not in [
                939549251522920468, # Yellow
                939551066234703972, # Green
                939581759023112223, # Black
                939581912379424809  # White
            ]: continue
            for emoji in guild.emojis:
                self.emojiGroups[emoji.name] = (emoji.animated, emoji.id)
            self.isEmojiLoaded = True


    @commands.command(description='게임 진행을 위한 인풋/명령어 입력 커맨드',
                      aliases = ['input', 'move'])
    async def play(self, ctx, gCmd:str = None):
        gGame, gLog = self.game.get(ctx.guild)
        if gGame is None:
            await ctx.send('No game playing!')
            return
        
        if gCmd is None:
            await ctx.send('Invalid input!')
            return

        result = gGame.update(gCmd)
        if isinstance(gGame, Wordle) and self.isEmojiLoaded and result[0] in [0, 1]:
            res = ''
            for i, c in enumerate(gCmd.upper().strip()):
                ename = f'{emojiToColor[result[1][i]]}_{c}'
                emoji = self.emojiGroups[ename]
                res += f'<:{ename}:{emoji[1]}>'
            gLog.append(res)
            await ctx.send('\n'.join(gLog))

            if result[0] == 1:
                await ctx.send(result[3])
            else:
                used = gGame.getUsed()
                await ctx.send(''.join(list(map(str, used))))
                usedlayout = ''
                for i in range(0, 26):
                    ename = f"{['Black', 'Yellow', 'Green', 'White'][used[i]]}_{chr(i+65)}"
                    emoji = self.emojiGroups[ename]
                    usedlayout += f'<:{ename}:{emoji[1]}>'
                await ctx.send(usedlayout)

        else:
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
            self.game[ctx.guild] = [Baseball(int(digits)), []]
            await ctx.send('The number is set, ready to play!')
        except:
            self.game[ctx.guild] = None
            await ctx.send('The number for digits is invalid!')


    @commands.command(description='워들')
    async def wordle(self, ctx, hard:str = 'Normal'):
        self.loadEmojis()
        if self.game.get(ctx.guild) is not None:
            await ctx.send('A game is already on play!')
            return
        try:
            self.game[ctx.guild] = [Wordle(hard.upper() == 'HARD'), []]
            await ctx.send('The word is chosen, ready to play!')
        except:
            self.game[ctx.guild] = None
            await ctx.send('Failed to create a wordle game...')


def setup(bot):
    bot.add_cog(minigames(bot))
