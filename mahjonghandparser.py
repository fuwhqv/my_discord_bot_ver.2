_letter1 = '만통삭'
_letter2 = '동남서북백발중'
_numbers = '123456789'

def _get_type_vals(type:str, vals:str):
    ret = []
    for val in vals:
        try:
            ret += [_letter1.index(type) * 9 + _numbers.index(val)]
        except: raise
    return ret

def _get_honor_vals(vals:str):
    ret = []
    for val in vals:
        try:
            ret += [_letter2.index(val) + 27]
        except: raise
    return ret

def parseHand(cmd:str):
    count  = [0] * 34
    iter   = 0
    last   = 0
    pvType = 1 # 0 for numbers, 1 for letter1, 2 for letter2
    tmpStr = ''

    try:
        for c in cmd:
            if   c in _numbers:
                iter   += 1
                pvType  = 0
                tmpStr += c

                if iter == 14:
                    last += _numbers.index(c)

            elif c in _letter1:
                if pvType != 0: raise
                pvType = 1
                for idx in _get_type_vals(c, tmpStr):
                    count[idx] += 1
                tmpStr = ''

                if iter == 14:
                    last += _letter1.index(c) * 9

            elif c in _letter2:
                if pvType == 0: raise
                iter  += 1
                pvType = 2
                for idx in _get_honor_vals(c):
                    count[idx] += 1

                if iter == 14:
                    last += _get_honor_vals(c)[0]
                
    except: raise

    if pvType == 0 or any(filter((4).__lt__, count)): raise
    count[last] -= 1

    ret = [4 * idx + i for idx, val in enumerate(count) for i in range(val)] + [4 * last + count[last]]
    if len(ret) != 14: raise

    return ret


def main():
    from mahjong.hand_calculating.hand import HandCalculator
    print('Press ctrl + c to quit.')
    while True:
        mInput = input('Mahjong hand input: ')
        try:
            hand = parseHand(mInput)
        except:
            print('Input is invalid.')
            continue

        calc = HandCalculator()
        result = calc.estimate_hand_value(hand, hand[-1])

        print(result.han, 'han:', result.yaku)
        print(hand)

if __name__ == '__main__':
    main()
