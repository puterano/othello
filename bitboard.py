NOLEFT = 0x820820820
NOUP = 0xfc0000000
NODOWN = 0x00000003f
NORIGHT = 0x041041041
from math import log

class Othelloboard():

    def __init__(self, white, black, playerwhite):
        self.white = white
        self.black = black
        self.placing = playerwhite
    
    def switch(self):
        self.placing = -self.placing

    def printboard(self):
        print('  ', end = '')
        for index in range(6):
            print(chr(ord('a') + index), end=' ')
        print()
        white = bin(self.white)[2:].zfill(36)
        black = bin(self.black)[2:].zfill(36)
        for digits in range(36):
            if digits % 6 == 0:
                print(digits // 6 + 1, end=' ')
            if white[digits] == '1':
                print('●', end = ' ')
            elif black[digits] == '1':
                print('○', end = ' ')
            else:
                print('-', end = ' ')
            if digits % 6 == 5:
                print()
    
    def printwithhint(self, locations = None):
        if not locations:
            locations = []
        star = bin(self.abletoplace())[2:].zfill(36)
        whiteboard = bin(self.white)[2:].zfill(36)
        blackboard = bin(self.black)[2:].zfill(36)
        print(' ', end = ' ')
        for i in range(6):
            print(chr(ord('a') + i), end = ' ')
        print()
        for index in range(36):
            if index % 6 == 0:
                print(index // 6 + 1, end = ' ')
            if whiteboard[index] == '1':
                print('●', end = ' ')
            elif blackboard[index] == '1':
                print('○', end = ' ')
            elif star[index] == '1':
                print('*', end = ' ')
            else:
                print('-', end = ' ')
            if index == 11 and locations:
                if locations[0][0] == 1:
                    print(f'    you will win in {locations[0][1]}', end = ' ')
                elif locations[0][0] == 0:
                    print(f'    you will draw in {locations[0][1]}', end = ' ')
                else:
                    print(f'    you will lose in {locations[0][1]}', end = ' ')
            elif index % 6 == 5 and index >= 23 and len(locations) >= index // 6 - 2:
                number = int(log(locations[index // 6 - 3][2], 2))
                match locations[index // 6 - 3][0]:
                    case 1:
                        sign = '+'
                    case -1:
                        sign = '-'
                    case other:
                        sign = '+-'
                print(f'      {chr(ord("f") - number % 6)}{6 - number // 6}: {sign}{locations[index // 6 - 3][1]}', end = ' ')
            if index % 6 == 5:
                print()

    def _search_for_place_location_in_direction(self, directionboard: int, leftorright: int, number_to_shift: int):
        potentialenemy = 0x000000000
        if self.placing == 1:
            board = self.white
            opponentboard = self.black
        else:
            board = self.black
            opponentboard = self.white
        temp = board
        for _ in range(6):
            temp &= ~directionboard
            if leftorright == 1:
                temp <<= number_to_shift
            else:
                temp >>= number_to_shift
            temp &= opponentboard
            potentialenemy |= temp
        potentialenemy &= ~directionboard
        if leftorright == 1:
            potentialenemy <<= number_to_shift
        else:
            potentialenemy >>= number_to_shift
        return potentialenemy & ~(board | opponentboard)
    
    def abletoplace(self):
        abletoplace = self._search_for_place_location_in_direction(NOLEFT, 1, 1)
        for i in {(NOUP, 1, 6), (NODOWN, -1, 6), (NORIGHT, -1, 1), 
                    (NOUP | NOLEFT, 1, 7), (NOUP | NORIGHT, 1, 5),
                    (NODOWN | NOLEFT, -1, 5), (NODOWN | NORIGHT, -1, 7)}:
            abletoplace |= self._search_for_place_location_in_direction(*i)
        return abletoplace
    
    def _search_for_invert_position_in_direction(self, location_to_place, leftorright, length_of_shift, masking_board):
        potentialplace = 0x000000000
        if self.placing == 1:
            playerboard = self.white
            opponentboard = self.black
        else:
            playerboard = self.black
            opponentboard = self.white
        for _ in range(6):
            location_to_place &= ~masking_board
            if leftorright == 1:
                location_to_place <<= length_of_shift
            else:
                location_to_place >>= length_of_shift
            if location_to_place & opponentboard != 0:
                location_to_place &= opponentboard
                potentialplace |= location_to_place
            else:
                if location_to_place & playerboard == 0:
                    potentialplace = 0x000000000
                break
        return potentialplace
    
    def invertboard(self, location):
        if self.placing == 1:
            self.white |= location
        else:
            self.black |= location
        for inputs in [(1,1,NOLEFT), (1,6,NOUP), (1,7,NOLEFT|NOUP), 
                        (1,5,NORIGHT|NOUP), (-1,1,NORIGHT), (-1,6,NODOWN), 
                        (-1,7,NODOWN|NORIGHT), (-1,5,NODOWN|NOLEFT)]:
            fornow = self._search_for_invert_position_in_direction(location, *inputs)
            if self.placing == 1:
                self.white |= fornow
                self.black ^= fornow
            else:
                self.black |= fornow
                self.white ^= fornow

    def get_winner(self):
        white_count = 0
        black_count = 0
        while self.white or self.black:

            if self.white & 1:
                white_count += 1
            if self.black & 1:
                black_count += 1

            self.white >>= 1
            self.black >>= 1
            
        if white_count > black_count:
            return 1
        elif black_count > white_count:
            return -1
        return 0