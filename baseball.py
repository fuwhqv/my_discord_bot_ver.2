import random
from datetime import datetime

random.seed(datetime.now())

class Baseball:
    def __init__(self, dig:int=3):
        self.digits = dig
        self.turn = 0

        self.number = '0'*self.digits
        while hasDup(self.number):
            self.number = str(random.randint(10**(self.digits-1), 10**self.digits-1))

    def __repr__(self):
        return 'Baseball'

    def update(self, gCmd:str):
        if not isValid(gCmd, self.digits):
            return [-1, 'Invalid input!']

        if hasDup(gCmd):
            return [-2, 'Input has duplicate digits!']

        self.turn += 1
        return self.getResult(gCmd)

    def getResult(self, val:str):
        s,b = 0,0

        for i in range(self.digits):
            for j in range(self.digits):
                if self.number[i]==val[j]:
                    if i==j:
                        s += 1
                    else:
                        b += 1

        if s == self.digits:
            return [1, ('Homerun! Finished in %d turns.'%self.turn)]
        return [0, ('Turn %2d: %ds %db'%(self.turn, s, b))]


def hasDup(num:str):
    for i in range(len(num)-1):
        for j in range(i+1, len(num)):
            if num[i]==num[j]:
                return True
    return False

def isValid(num:str, dig:int):
    try:
        tmp = int(num)
        if len(num) != dig or not(tmp >= 10**(dig-1) and tmp <= 10**dig-1):
            raise
    except:
        return False
    return True

if __name__ == '__main__':
    game = Baseball(3)
    print(game.update('123'))
    print(game.update('456'))
    print(game.update('789'))
    print(game.update('1234'))
    print(game.update('1 23'))
    print(game.update('abc'))
    print(game.update('100'))