from random import choice
import os

words_path =  os.path.join(os.getcwd(), 'minigames', 'sgb-words.txt')

upperRange = range(65, 91)
class Wordle:
    def __init__(self, isHard:bool = False):
        self.words = None
        self.loadWords()
        self.newGame(isHard)


    def loadWords(self):
        if self.words is not None: return
        with open(words_path, 'r') as words:
            self.words = words.readlines()
        self.words = list(map(lambda x: x.upper().strip(), self.words))


    def getNewWord(self):
        self.word = choice(self.words).strip().upper()


    def newGame(self, isHard:bool = False):
        self.tries     = 0
        self.alphabets = [[0]*5 for _ in range(26)]
        self.isHard    = isHard
        self.lastCounts= [0] * 26
        self.black     = [False] * 26
        self.getNewWord()


    def __isValidLetter(self, c:str):
        if c is None: return False
        if len(c) != 1: return False
        if ord(c) not in upperRange: return False
        return True


    def isValidWord(self, w:str):
        if w is None: return False
        if len(w) != 5: return False
        for c in w:
            if not self.__isValidLetter(c): return False
        if w not in self.words: return False

        return True


    def isValidWordHard(self, w:str):
        for alpha, alist in enumerate(self.alphabets):
            pos = []

            for idx, val in enumerate(alist):
                if val == 2:
                    pos.append(idx)

            # revealed green letters should have same position
            for p in pos:
                if chr(alpha+65) != w[p]: return False

        # green + yellow letters should appear not less than before
        counts = [0] * 26
        for c in w:
            counts[ord(c)-65] += 1
        for a, b in zip(self.lastCounts, counts):
            if a > b: return False

        return True


    def compare(self, w:str):
        if not self.isValidWord(w): return 1, None
        if self.isHard and (not self.isValidWordHard(w)): return 2, None

        result   = [0] * 5
        appeared = [False] * 5
        black    = [True ] * 5
        counts   = [0] * 26
    
        #checks for same position
        for i in range(5):
            if w[i] != self.word[i]: continue

            appeared[i] = True
            black[i] = False
            result[i] = 2
            self.alphabets[ord(w[i])-65][i] = 2
            counts[ord(w[i])-65] += 1

        #checks for different position
        for i in range(5):
            if result[i] != 0: continue

            for _j in range(1, 5):
                j = (i+_j)%5

                if w[i] != self.word[j]: continue
                if appeared[j]: continue

                appeared[j] = True
                black[i] = False
                result[i] = 1
                self.alphabets[ord(w[i])-65][i] = 1
                counts[ord(w[i])-65] += 1

        for i in range(5):
            if not black[i]: continue
            self.black[ord(w[i])-65] = True

        self.lastCounts = counts
        self.tries += 1
        return 0, result


    def update(self, gCmd:str): # a wrapper method for my discord bot
        ret, res = self.compare(gCmd.strip().upper())
        msg = f"Word{'*' if self.isHard else ''}: {gCmd.lower().strip()}"
        if     ret  ==  1: return [-1, 'The input is invalid!']
        if     ret  ==  2: return [-2, 'All revealed hints must be used!']
        if sum(res) == 10: return [ 1, '🟩🟩🟩🟩🟩', msg, f'Finished in {self.tries} tries{" with hard mode" if self.isHard else ""}.']
        st = ''
        for i in res:
            st += ['⬛', '🟨', '🟩'][i]
        
        greens = '🟩: '
        yellows= '🟨: '
        blacks = '⬛: '

        for idx, alist in enumerate(self.alphabets):
            if   2 in alist:
                greens  += chr(idx + 65)
                self.black[idx] = False
            elif 1 in alist:
                yellows += chr(idx + 65)
                self.black[idx] = False
        
        for idx, val in enumerate(self.black):
            if not val: continue
            blacks += chr(idx + 65)

        return [0, st, msg, '\n'.join([greens, yellows, blacks])]


def main():
    wordle = Wordle(True)

    while True:
        word = input('5 Letters word input: ')
        word = word.upper().strip()
        retcode, result = wordle.compare(word)

        if result is not None:
            for i in result: print('.?!'[i], end='')
            print()

        if result is not None and sum(result) == 10: break


if __name__=='__main__':
    main()
