from typing import Iterable
from random import choice
import os

words_path =  os.path.join(os.getcwd(), 'sgb-words.txt')

class WordleBase:
    def __init__(self, isHard:bool = False, length:int = 5, kinds:int = 26):
        self.words  = None
        self.length = length
        self.kinds  = kinds
        self._loadWords()
        self.newGame(isHard)

    def _loadWords(self):
    #overidable
        if self.words is not None: return
        with open(words_path, 'r') as words:
            self.words = words.readlines()
        self.words = list(map(lambda x: x.upper().strip(), self.words))

    def _setNewWord(self):
    #overidable
        self.word = choice(self.words).upper().strip()
        #self.word = ''.join([chr(65+i) for i in range(self.length)]).upper().strip()
        #self.word = 'SEDER'

    def _getIndexOf(self, c:str):
    #overidable
        return (ord(c)-65)

    def newGame(self, isHard:bool):
        self.tries  = 0
        self.isHard = isHard
        self.status = [   -1] * self.kinds

        if self.isHard:
            self.greens = [False] * self.length
            self.counts = [    0] * self.kinds

        self._setNewWord()

    def isValid(self, word:str):
    #overidable
        if word is None: return False
        if len(word) != self.length: return False
        if any(map(lambda c: ord(c) not in range(65, 91), word)): return False
        if word not in self.words: return False
        return True

    def isHardValid(self, word:Iterable):
        # Revealed green should stay at same position
        for idx in range(self.length):
            if not self.greens[idx]: continue
            if self.word[idx] != word[idx]: return False

        # green + yellow should appear not less than before
        counts = [0] * self.kinds
        for c in word:
            counts[self._getIndexOf(c)] += 1

        if any(map(lambda target, guessd: target > guessd, \
            self.counts, counts)): return False

        return True

    def _elementNE(self, e1, e2):
        return e1!=e2

    def compare(self, word:Iterable):
        if not self.isValid(word): return 1, None
        if self.isHard and not self.isHardValid(word): return 2, None

        alUsed = [False] * self.length
        result = [    0] * self.length

        if self.isHard:
            counts = [0] * self.kinds

        # check greens
        for idx in range(self.length):
            if self._elementNE(word[idx], self.word[idx]): continue

            result[idx] = 2
            alUsed[idx] = True
            self.status[self._getIndexOf(word[idx])] = 2

            if self.isHard:
                counts[self._getIndexOf(word[idx])]  += 1
                self.greens[idx] = True

        # check yellows
        for idx_guessd in range(self.length):
            if result[idx_guessd] != 0: continue

            for it in range(1, self.length):
                idx_target = (idx_guessd + it) % self.length

                if self._elementNE(
                    word[idx_guessd],
                    self.word[idx_target]
                ): continue
                if alUsed[idx_target]: continue

                result[idx_guessd] = 1
                alUsed[idx_target] = True
                self.status[self._getIndexOf(word[idx_guessd])] = max(
                    self.status[self._getIndexOf(word[idx_guessd])],
                    1
                )

                if self.isHard:
                    counts[self._getIndexOf(word[idx_guessd])] += 1

                break

        # register blacks
        for idx in range(self.length):
            if result[idx] != 0: continue

            self.status[self._getIndexOf(word[idx])] = max(
                self.status[self._getIndexOf(word[idx])],
                0
            )

        self.tries += 1
        if self.isHard: self.counts = counts

        return 0, result


class Wordle(WordleBase):
    def update(self, gCmd:str):
        ret, res = self.compare(gCmd.upper().strip())
        if ret == 0 and sum(res) == 10:
            ret = -1
        return {
            'ret'   : -ret,
            'isHard': self.isHard,
            'input' : gCmd.upper().strip(),
            'res'   : res,
            'tries' : self.tries,
            'used'  : self.status
        }


def main():
    wordle = Wordle(True)

    while True:
        word = input('5 Letters word input: ')
        word = word.upper().strip()
        _, result = wordle.compare(word)

        if result is not None:
            for i in result: print('.?!'[i], end='')
        else:
            print(f'err:{_}', end='')
        print(f"[{wordle.word}]")

        if result is not None and sum(result) == 10: break


if __name__=='__main__':
    main()
