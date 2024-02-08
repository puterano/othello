import bitboard
import itertools

def list_to_bitboard(board: list[list[str]], placing: int):
    white = 0
    black = 0
    for locations in itertools.chain.from_iterable(board):
        white <<= 1
        black <<= 1
        if locations == '●':
            white += 1
        elif locations == '○':
            black += 1
    return bitboard.Othelloboard(white, black, placing)

# field = [['']*6 for _ in range(6)]

# field[0] = '- - ● ● ● -'.split(' ')
# field[1] = '- - ○ ○ ○ -'.split(' ')
# field[2] = '○ ○ ● ○ ○ ○'.split(' ')
# field[3] = '- ○ ○ ● ○ ○'.split(' ')
# field[4] = '- - ● ● ● ○'.split(' ')
# field[5] = '- - - - - -'.split(' ')

BEST_WHITE_15_LEFT = bitboard.Othelloboard(15034499968, 249409600, 1)

# field[0] = '- - - - - -'.split(' ')
# field[1] = '- - - - - -'.split(' ')
# field[2] = '- - ● ○ - -'.split(' ')
# field[3] = '- - ○ ● - -'.split(' ')
# field[4] = '- - - - - -'.split(' ')
# field[5] = '- - - - - -'.split(' ')

INITIAL = bitboard.Othelloboard(2113536, 1081344, -1)

# field[0] = '- - ● ○ - -'.split(' ')
# field[1] = '- - ○ ○ - -'.split(' ')
# field[2] = '○ ○ ● ○ ○ ○'.split(' ')
# field[3] = '- ○ ○ ● ○ ○'.split(' ')
# field[4] = '- * ● ● ● ○'.split(' ')
# field[5] = '- * - - - -'.split(' ')

BEST_WHITE_17_LEFT = bitboard.Othelloboard(8592049024, 4510822464, 1)

def main():
    print(BEST_WHITE_17_LEFT.white, BEST_WHITE_17_LEFT.black)
if __name__ == '__main__':
    main()