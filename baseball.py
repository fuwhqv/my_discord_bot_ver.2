from wordle import WordleBase
from random import randint

class Baseball(WordleBase):
    def __init__(self, len:int = 3):
        super().__init__(True, len, 10)

    def _loadWords(self):
        pass

    def _setNewWord(self):
        word = str(randint(100, 999))
        while not self.isHardValid(word):
            word = str(randint(100, 999))
        self.word = word

    def _getIndexOf(self, c:str):
        return int(c)

    def isValid(self, word:str):
        try:
            val = int(word)
            return val >= 100 and val < 1000
        except:
            return False

    def isHardValid(self, word:str):
        if word[0] == '0': return False

        for i in range(self.length):
            for j in range(self.length):
                if i==j: continue
                if word[i] == word[j]: return False

        return True

    def update(self, gCmd:str):
        ret, res = self.compare(gCmd)
        if ret == 0 and sum(res) == 2 * self.length:
            ret = -1
        return {
            'ret'  : -ret,
            'input': gCmd,
            'res'  : res,
            'tries': self.tries
        }


def main():
    wordle = Baseball()

    while True:
        word = input('3 Digits number input: ').strip()
        _, result = wordle.compare(word)

        if result is not None:
            s = sum(map(lambda x: 1 if x==2 else 0, result))
            b = sum(map(lambda x: 1 if x==1 else 0, result))
            print(f"Turn {wordle.tries:>2}: {s}s {b}b")
            print(result)
        else:
            print(f"err:{_}", end='')
        print(f"[{wordle.word}]")
        print(wordle.status)

        if result is not None and sum(result) == wordle.length * 2: break


if __name__ == '__main__':
    main()
