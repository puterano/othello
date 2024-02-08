NOLEFT = ~0x820820820
NOUP = ~0xfc0000000
NODOWN = ~0x00000003f
NORIGHT = ~0x041041041

from math import log
import time
total_time = 0
timed = 0

class Othelloboard():

    def __init__(self, white, black, playerwhite):
        # global total_time
        # global timed
        # timed += 1

        # start = time.time()
        self.white = white
        self.black = black
        self.placing = playerwhite

        # total_time += time.time() - start


    def switch(self):
        self.placing = -self.placing

    def printboard(self):
        field = [['']*6 for _ in range(6)]
        white, black = self.white, self.black
        location = 0
        for location in range(36):

            if white & 1:
                field[-(location // 6 + 1)][-(location % 6 + 1)] = '●'
            elif black & 1:
                field[-(location // 6 + 1)][-(location % 6 + 1)] = '○'
            else:
                field[-(location // 6 + 1)][-(location % 6 + 1)] = '-'

            white >>= 1
            black >>= 1
        
        print(' ', end = ' ')
        for index in range(6):
            print(chr(ord('a') + index), end = ' ')
        print()

        for line_number, line in enumerate(field):
            print(line_number + 1, end = ' ')
            for cells in line:
                print(cells, end = ' ')
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
            temp &= directionboard
            if leftorright == 1:
                temp <<= number_to_shift
            else:
                temp >>= number_to_shift
            temp &= opponentboard
            potentialenemy |= temp
        potentialenemy &= directionboard
        if leftorright == 1:
            potentialenemy <<= number_to_shift
        else:
            potentialenemy >>= number_to_shift
        return potentialenemy & ~(board | opponentboard)
    
    def abletoplace(self):
        # global total_time
        # global timed
        # start = time.time()
        # timed += 1

        abletoplace = self._search_for_place_location_in_direction(NOLEFT, 1, 1)
        for i in {(NOUP, 1, 6), (NODOWN, -1, 6), (NORIGHT, -1, 1), 
                    (NOUP & NOLEFT, 1, 7), (NOUP & NORIGHT, 1, 5),
                    (NODOWN & NOLEFT, -1, 5), (NODOWN & NORIGHT, -1, 7)}:
            abletoplace |= self._search_for_place_location_in_direction(*i)

        # total_time += time.time() - start
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
            location_to_place &= masking_board
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
        # global total_time
        # global timed
        # start = time.time()
        # timed += 1

        if self.placing == 1:
            self.white |= location
        else:
            self.black |= location
        for inputs in [(1,1,NOLEFT), (1,6,NOUP), (1,7,NOLEFT & NOUP), 
                        (1,5,NORIGHT & NOUP), (-1,1,NORIGHT), (-1,6,NODOWN), 
                        (-1,7,NODOWN & NORIGHT), (-1,5,NODOWN & NOLEFT)]:
            fornow = self._search_for_invert_position_in_direction(location, *inputs)
            if self.placing == 1:
                self.white |= fornow
                self.black ^= fornow
            else:
                self.black |= fornow
                self.white ^= fornow
        
        # total_time += time.time() -start


    def get_winner(self): # became little faster -- 0.09 -> 0.01 to 0.04
        
        global total_time
        # global timed
        start = time.time()
        # timed += 1
        
        self.white = self.white - ((self.white >> 1) & 0x555555555)
        self.black = self.black - ((self.black >> 1) & 0x555555555)
        
        self.white = (self.white & 0x333333333) + ((self.white >> 2) & 0x333333333)
        self.black = (self.black & 0x333333333) + ((self.black >> 2) & 0x333333333)
        
        self.white = (self.white + (self.white >> 4)) & 0xf0f0f0f0f
        self.black = (self.black + (self.black >> 4)) & 0xf0f0f0f0f
        
        self.white = self.white + (self.white >> 8)
        self.black = self.black + (self.black >> 8)
        
        self.white = self.white + (self.white >> 16)
        self.black = self.black + (self.black >> 16)
        
        self.white = self.white + (self.white >> 32)
        self.black = self.black + (self.black >> 32)
        
        self.white, self.black = self.white & 63, self.black & 63

        total_time += time.time() - start

        if self.white > self.black:
            return 1
        elif self.white < self.black:
            return -1
        else:
            return 0