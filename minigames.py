from discord.ext import commands
from baseball    import Baseball
from wordle      import Wordle
from madle       import Madle

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
                939549251522920468, # Yellow alphabets
                939551066234703972, # Green  alphabets
                939581759023112223, # Black  alphabets
                939581912379424809, # White  alphabets

                942009567750004746, # White  mahjong tiles
                942001041346539550, # Ornage mahjong tiles
                942001446889603092, # Green  mahjong tiles
            ]: continue
            for emoji in guild.emojis:
                self.emojiGroups[emoji.name] = (emoji.animated, emoji.id)
            self.isEmojiLoaded = True


    @commands.command(description='게임 진행을 위한 인풋/명령어 입력 커맨드',
                      aliases = ['input', 'move'])
    async def play(self, ctx, *gArgs):
        gCmd:str = ' '.join(gArgs)
        gGame, gLog = self.game.get(ctx.guild)

        if gGame is None:
            await ctx.send('No game playing!')
            return

        if gCmd == '':
            await ctx.send('Invalid input!')
            return

        result = gGame.update(gCmd)

        if   isinstance(gGame, Madle):
            await self._result_madle(ctx, gLog, result)
            return

        if isinstance(gGame, Wordle):
            await self._result_wordle(ctx, gLog, result)
            return

        if isinstance(gGame, Baseball):
            await self._result_baseball(ctx, gLog, result)
            return
    @commands.command(description='숫자야구(3~4자리)',
                      aliases=['baseball'])
    async def numberBaseball(self, ctx, digits:str ='3'):
        print(digits)
        if self.game.get(ctx.guild) is not None:
            await ctx.send('A game is already on play!')
            return
        try:
            self.game[ctx.guild] = [Baseball(int(digits)), []]
            await ctx.send('The number is set, ready to play!')
        except Exception as e:
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


    @commands.command(description='워들 마작 ver.')
    async def madle(self, ctx):
        self.loadEmojis()
        if self.game.get(ctx.guild) is not None:
            await ctx.send('A game is already on play!')
            return
        try:
            self.game[ctx.guild] = [Madle(), []]
            await ctx.send('A mahjong hand is chosen, ready to play!')
        except:
            self.game[ctx.guild] = None
            await ctx.send('Failed to create a madle game...')



    async def _result_wordle(self, ctx, gLog, result):
        # error handling
        if result['ret'] < 0:
            if result['ret'] == -1:
                await ctx.send('The input is invalid!')
            if result['ret'] == -2:
                await ctx.send('All revealed hint must be used!')
            return

        colors = ['Black', 'Yellow', 'Green', 'White']

        # printing input logs
        res = ''
        for idx, c in enumerate(result['input']):
            val   = result['res'][idx]
            ename = f'{colors[val]}_{c}'
            emoji = self.emojiGroups[ename]
            res  += f'<:{ename}:{emoji[1]}>'
        gLog.append(res)
        await ctx.send('\n'.join(gLog))

        # if finished
        if result['ret'] == 1:
            await ctx.send(
                f"Finished in {result['tries']} tries"
                f"{'with hard mode ' if result['isHard'] else ''}."
            )
            self.game[ctx.guild] = None
            return

        # printing used status
        usedLayout = '['
        for i in range(26):
            if i==13: usedLayout += ']\n['
            ename = f"{colors[result['used'][i]]}_{chr(i+65)}"
            emoji = self.emojiGroups[ename]
            usedLayout += f'<:{ename}:{emoji[1]}>'
        usedLayout += ']'
        await ctx.send(usedLayout)


    async def _result_madle(self, ctx, gLog, result):
        # error handling
        if result['ret'] < 0:
            if   result['ret'] == -1:
                await ctx.send('The input is invalid!')
            elif result['ret'] == -2:
                await ctx.send("There's no yaku in hand!")
            return

        colors = ['white', 'orange', 'green', 'white']

        # printing input logs
        res = ''
        print(result)
        for idx, num in enumerate(result['input']):
            val = result['res'][idx]
            ename = f"m{num//4 if val > 0 else 99:02}_{colors[val]}"
            emoji = self.emojiGroups[ename]
            if idx == 13: res += ' Win: '
            res += f'<:{ename}:{emoji[1]}>'
        gLog.append(res)

        for log in gLog:
            await ctx.send(log)

        # if finished
        if result['ret'] == 1:
            await ctx.send(
                f"Finished in {result['tries']} tries"
                f"{'with hard mode ' if result['isHard'] else ''}."
            )
            self.game[ctx.guild] = None
            return

        # if not finished in 6 tries
        if result['tries'] == 6:
            pass

        # printing used status
        usedLayout = '['
        for i in range(34):
            if i in [9, 18, 27]: usedLayout += ']\n['
            if i == 27: usedLayout += ':black_large_square:'
            if result['used'][i] == 0:
                ename = 'm99_white'
            else:
                ename = f"m{i:02}_{colors[result['used'][i]]}"
            emoji = self.emojiGroups[ename]
            usedLayout += f'<:{ename}:{emoji[1]}>'
        usedLayout += ':black_large_square:]'
        await ctx.send(usedLayout)


    async def _result_baseball(self, ctx, gLog, result):
        # error handling
        if result['ret'] < 0:
            if result['ret'] == -1:
                await ctx.send('The input is invalid!')
            if result['ret'] == -2:
                await ctx.send('The input has duplicates!')
            return # error handling needed

        if result['ret'] == 1:
            await ctx.send(f"Homerun! Finished in {result['tries']} turns.")
            self.game[ctx.guild] = None
            return

        s = sum(lambda x: 1 if x==2 else 0, result['res'])
        b = sum(lambda x: 1 if x==1 else 0, result['res'])

        await ctx.send(f"Turn {result['tries']:>2}: {s}s {b}b")

def setup(bot):
    bot.add_cog(minigames(bot))
