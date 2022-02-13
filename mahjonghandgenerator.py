from random import shuffle, choice, choices
from mahjong.hand_calculating.hand import HandCalculator

calc = HandCalculator()

def _generate_triplet(used): # 25%
    used[choice(range(34))] += 3

def _generate_sequence(used): # 75%
# 0  1  2  3  4  5  6 |  7  8
# 9 10 11 12 13 14 15 | 16 17
#18 19 20 21 22 23 24 | 25 26
#
#7 => 9, 8 => 10, ... 13 => 15, 14 => 18, 15 => 19, ...
#x + (x // 7)*2
    target = choice(list(map(lambda x: x + (x//7)*2, list(range(21)))))
    used[target  ] += 1
    used[target+1] += 1
    used[target+2] += 1

def _generate_head(used):
    used[choice(range(34))] += 2

def get_normal_hand():
    while True:
        count = [0] * 34

        for _ in range(4): # generates 4 bodies
            choices([_generate_triplet, _generate_sequence], weights = [1, 3])[0](count)

        # generates a head
        _generate_head(count)

        if any(filter((4).__lt__, count)): continue
        break

    ret = []

    for idx, val in enumerate(count):
        for i in range(val):
            ret.append(4*idx + i)
    shuffle(ret)

    return sorted(ret[:-1])+ [ret[-1]]

def get_thirteen_orphans(): # 0.04%
    ret = list(map(lambda x: x*4, [0, 8, 9, 17, 18, 26] + list(range(27, 34))))
    ret += [choice(ret)]
    shuffle(ret)

    return sorted(ret[:-1]) + [ret[-1]]

def get_seven_pairs(): # 2.50%
    ret = list(map(lambda x: x*4, range(34)))
    shuffle(ret)

    ret = ret[:7]
    ret += list(map(lambda x: x+1, ret))
    shuffle(ret)

    return sorted(ret[:-1]) + [ret[-1]]

def generate_hand():
    func = choices([get_thirteen_orphans, get_seven_pairs, get_normal_hand], cum_weights=[0.04, 2.54, 100])[0]
    hand = func()
    
    while True:
        result = calc.estimate_hand_value(hand, hand[-1])
        
        if result.yaku is not None and len(result.yaku) > 0: break
        hand = func()

    return hand


'''
0~135
0,1,2,3  4,5,6,7  8,9,10,11 ... 132,133,134,135  //4
0,0,0,0  1,1,1,1  2,2, 2, 2 ...  33, 33, 33, 33  map(x + (x//9))
 0,  1,  2, ... ,  8,
10, 11, 12, ... , 18,
'''

def main():
    while True:
        hand = generate_hand()
        result = calc.estimate_hand_value(hand, hand[-1])

        yaku = list(map(str, result.yaku))
        if result.han >= 13 and 'Suu ankou tanki' not in yaku and 'Kokushi Musou' not in yaku and 'Kokushi Musou Juusanmen Matchi' not in yaku: break

    print(result.han, 'han:', result.yaku)
    print(hand)


if __name__ == '__main__':
    main()
