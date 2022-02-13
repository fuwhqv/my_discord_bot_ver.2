from mahjong.hand_calculating.hand_config import HandConfig
from mahjonghandgenerator                 import generate_hand, calc
from mahjonghandparser                    import parseHand
from wordle                               import WordleBase
from random                               import randint

class Madle(WordleBase):
    def __init__(self, isHard:bool = False):
        super().__init__(isHard, 14, 34)

    def _loadWords(self):
        pass

    def _setNewWord(self):
        self.word = generate_hand()
        self.wind_player = randint(27, 30)
        self.wind_round  = randint(27, 30)
        print(self.word)

    def _getIndexOf(self, num:int):
        return num//4

    def isValid(self, hand:list):
        result = calc.estimate_hand_value(hand, hand[-1],
            config = HandConfig(player_wind = self.wind_player, round_wind = self.wind_round)
        )
        print(result)
        if result.yaku is not None and len(result.yaku) > 0: return True
        return False

    def update(self, gCmd:str):
        try: hand = parseHand(gCmd)
        except: return {'ret': -1}

        ret, res = self.compare(hand)
        if ret == 0 and sum(res) == 28:
            ret = -1
        return {
            'ret'   : -ret,
            'isHard': self.isHard,
            'input' : hand,
            'res'   : res,
            'tries' : self.tries,
            'used'  : self.status
        }

    def _elementNE(self, e1:int, e2:int):
        return (e1//4) != (e2//4)


def test2():
    madle = Madle()
    
    while True:
        hand = input('Winning mahjong hand input: ')
        try:
            hand = parseHand(hand)
            _, result = madle.compare(hand)
            if result is not None:
                for i in result: print('.?!'[i], end='')
            else:
                print(f"err:{_}", end='')
            print(f"{madle.word}")
            print(madle.status)
            if result is not None and sum(result) == madle.length * 2: break

        except:
            print('Invalid input')
        
        print(hand)


if __name__ == '__main__':
    test2()
