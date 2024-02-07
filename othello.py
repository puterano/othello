
NOLEFT = 0x820820820
NOUP = 0xfc0000000
NODOWN = 0x00000003f
NORIGHT = 0x041041041
from time import sleep, time
from math import log


def validinput(ask, wrong, *valids):
    while True:
        inputted = input(ask)
        if inputted not in set(valids):
            print(wrong)
            sleep(0.8)
        else:
            break
    return inputted


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

    def search_for_place_location_in_direction(self, directionboard: int, leftorright: int, number_to_shift: int):
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
        abletoplace = self.search_for_place_location_in_direction(NOLEFT, 1, 1)
        for i in {(NOUP, 1, 6), (NODOWN, -1, 6), (NORIGHT, -1, 1), 
                    (NOUP | NOLEFT, 1, 7), (NOUP | NORIGHT, 1, 5),
                    (NODOWN | NOLEFT, -1, 5), (NODOWN | NORIGHT, -1, 7)}:
            abletoplace |= self.search_for_place_location_in_direction(*i)
        return abletoplace
    
    def search_for_invert_position_in_direction(self, location_to_place, leftorright, length_of_shift, masking_board):
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
            fornow = self.search_for_invert_position_in_direction(location, *inputs)
            if self.placing == 1:
                self.white |= fornow
                self.black ^= fornow
            else:
                self.black |= fornow
                self.white ^= fornow


def returnbasedonsize(grade1, grade2, bigger = True):
    if grade1[0] > grade2[0]:
        returning = grade1
    elif grade1[0] == grade2[0]:
        if grade1[0] == 1 and grade1[1] <= grade2[1]:
            returning = grade1
        elif grade1[0] != 1 and grade1[1] >= grade2[1]:
            returning = grade1
        else:
            returning = grade2
    else:
        returning = grade2
    if bigger == True:
        return returning
    else:
        if returning == grade1:
            return grade2
        else:
            return grade1


def findextreme(board:Othelloboard, minrequire, maxcap, self, abletoplace_ = 0):
    #if self == -1:
    #    printboard(placerboard, opponentboard)
    #else:
    #    printboard(opponentboard, placerboard)
    #input(self)
    # nonlocal traversed
    # traversed += 1
    # board.printboard()
    # input(board.placing)
    # input(board.white)
    # input(board.black)
    # input(board.abletoplace())
    # newboard = Othelloboard(65497161409, 1074831678, -1)
    # print('newboard', newboard.abletoplace())
    if not abletoplace_:
        possiblelocation = board.abletoplace()
    else:
        possiblelocation = abletoplace_
    if not possiblelocation:
        temp = Othelloboard(board.white, board.black, board.placing)
        temp.switch()
        gotonext = temp.abletoplace()
        if gotonext:
            return findextreme(temp, minrequire, maxcap, -self, gotonext)
        else:
            whitecount = 0
            blackcount = 0
            while temp.white != 0 or temp.black != 0:
                whitecount += temp.white & 1
                blackcount += temp.black & 1
                temp.white >>= 1
                temp.black >>= 1
            #self 1 placing 1 - placing white, my turn - i am white
            #self 1 placing -1  - placing black, my turn - i am black
            #self -1 placing 1 - placing white, opponent turn - i am black
            #self -1 placing -1  - placing black, opponent turn - i am white
            if self * -temp.placing * whitecount > self * -temp.placing * blackcount:
                #input('winreturn')
                return (1, 1)
            elif whitecount != blackcount:
                #input('losereturn')
                return (-1, 1)
            else:
                #input('drawreturn')
                return (0, 1)
    else:
        minrequire = (minrequire[0], minrequire[1] - 1)
        maxcap = (maxcap[0], maxcap[1] - 1)
        onlylocation = 1
        extreme = (-self, 0)
        while possiblelocation != 0:
            if possiblelocation & 1 != 0:
                temp = Othelloboard(board.white, board.black, board.placing)
                temp.invertboard(onlylocation)
                temp.switch()
                value = findextreme(temp, minrequire, maxcap, -self)
                extreme = returnbasedonsize(extreme, value, bool(self + 1))
                if self == 1:
                    minrequire = returnbasedonsize(value, minrequire, True)
                else:
                    maxcap = returnbasedonsize(value, maxcap, False)
            if returnbasedonsize(maxcap, minrequire, True) == minrequire:
                break
            onlylocation <<= 1
            possiblelocation >>= 1
        return (extreme[0], extreme[1] + 1)


def returnlists(board:Othelloboard):
    returninglist = []
    possiblelocation = board.abletoplace()
    onlylocation = 1
    while possiblelocation != 0:
        if possiblelocation & 1 != 0:
            temp = Othelloboard(board.white, board.black, board.placing)
            temp.invertboard(onlylocation)
            #input()
            #printboard(tempplacer, tempopponent)
            temp.switch()
            value = findextreme(temp, (-1, 0), (1, 0), -1)
            # temp.printboard()
            # input(value)
            # input(f'{temp.white}, {temp.black}, {temp.placing}')
            #input(str(onlylocation) + str(value))
            wheretoinsert = -1
            for index, existingvalue in enumerate(returninglist):
                if returnbasedonsize((existingvalue[0], existingvalue[1]), (value[0], value[1]), True) == value:
                    wheretoinsert = index
                    break
            if wheretoinsert == -1:
                returninglist.append((value[0], value[1], onlylocation))
            else:
                returninglist.insert(wheretoinsert, (value[0], value[1], onlylocation))
        onlylocation <<= 1
        possiblelocation >>= 1
    return returninglist


def play():
    print('let\'s play 6*6 reversi!')
    sleep(0.8)
    aiplacing = -1
    if validinput('do you want to play solo or with ai? ', 'please enter solo or ai', 'solo', 'ai') == 'ai':
        if validinput('do you want to go first or second? ', 'please enter first or second', 'first', 'second') == 'first':
            aiplacing = 0
        else:
            aiplacing = 1
    if validinput('do you want to know the best moves? ', 'please enter yes or no', 'yes', 'no') == 'yes':
        best = 0
    else:
        best = 1
    placerboard = 0x000204000
    opponentboard = 0x000108000
    def listtobitboard(board: list[list[int]]) -> (int, int):
        white = 0
        black = 0
        for rows in board:
            for cells in rows:
                white <<= 1
                black <<= 1
                if cells == '●':
                    white += 1
                elif cells == '○':
                    black += 1
        return white, black
    field = [[]]*6
    field[0] = '- - ● ● ● -'.split(' ')
    field[1] = '- - ○ ○ ○ -'.split(' ')
    field[2] = '○ ○ ● ○ ○ ○'.split(' ')
    field[3] = '- ○ ○ ● ○ ○'.split(' ')
    field[4] = '- - ● ● ● ○'.split(' ')
    field[5] = '- - - - - -'.split(' ')
    # field[0] = '● ● - ○ ● ●'.split(' ')
    # field[1] = '● - ● ● - ●'.split(' ')
    # field[2] = '● ○ ● ● ○ ●'.split(' ')
    # field[3] = '● ● ○ ● ● ○'.split(' ')
    # field[4] = '● ● ● ○ ● ●'.split(' ')
    # field[5] = '● ● ○ ● ○ ●'.split(' ')
    # field[0] = '● ● ● ● - ○'.split(' ')
    # field[1] = '- - ○ ○ ○ -'.split(' ')
    # field[2] = '○ ○ ● ○ ○ ○'.split(' ')
    # field[3] = '● ● ● ● ● ○'.split(' ')
    # field[4] = '● ● ● ● ● ●'.split(' ')
    # field[5] = '○ ○ ○ ○ - -'.split(' ')
    # field[0] = '● ● ● ● - ○'.split(' ')
    # field[1] = '● ● ○ ○ ○ -'.split(' ')
    # field[2] = '● ● ● ○ ○ ○'.split(' ')
    # field[3] = '● ● ○ ● ○ ○'.split(' ')
    # field[4] = '● ● ● ○ ● ●'.split(' ')
    # field[5] = '○ ○ ○ ○ ○ ●'.split(' ')
    # field[0] = '● ● ● ● ● ●'.split(' ')
    # field[1] = '● ● ● ● ● ●'.split(' ')
    # field[2] = '● ● ● ● ● ●'.split(' ')
    # field[3] = '● ● ● ● ● ●'.split(' ')
    # field[4] = '● ● ● ● ● ●'.split(' ')
    # field[5] = '● ● ● - ○ ●'.split(' ')
    # print(listtobitboard(field))
    # input()
    board = Othelloboard(*listtobitboard(field), 1)
    # print(board.white)
    # print(board.black)
    # input()
    # newboard = Othelloboard(65497161409, 1074831678, -1)
    # board = Othelloboard(placerboard, opponentboard, -1)
    # print('oldboard', newboard.abletoplace())
    locationslist = []
    for rows in range(6):
        for columns in range(6):
            locationslist.append(chr(ord('a') + rows) + str(columns + 1))
    board.printboard()
    while True:
        sleep(0.8)
        placingcolor = chr((ord('●') + ord('○')) // 2 + (ord('●') - ord('○')) * board.placing // 2)
        opponentcolor = chr((ord('●') + ord('○')) // 2 - (ord('●') - ord('○')) * board.placing // 2)
        if board.abletoplace():
            # findextreme(newboard, (-1, 0), (1, 0), 1)
            if aiplacing <= 0:
                # findextreme(newboard, (-1, 0), (1, 0), 1)
                if best == 0:
                    returned = returnlists(board)
                    board.printwithhint(returned)
                else:
                    board.printwithhint()
                placelocation = (validinput(placingcolor + ': where do you want to place? ', 
                                                'please input valid location', *locationslist))
                placelocation = 2**(6 * (6 - int(placelocation[1])) + ord('f') - ord(placelocation[0]))
                while not placelocation & board.abletoplace():
                    print('you cannot place there!')
                    sleep(0.8)
                    board.printwithhint()
                    sleep(0.8)
                    placelocation = (validinput(placingcolor + ': where do you want to place? ', 
                                                'please input valid location', *locationslist))
                    placelocation = 2**(6 * (6 - int(placelocation[1])) + ord('f') - ord(placelocation[0]))
            else:
                board.printwithhint()
                #traversed = 0
                print('ai is thinking...')
                start = time()
                returned = returnlists(board)
                end = time()
                #print(traversed)
                if (end - start) < 0.8:
                    sleep(0.8 - (end - start))
                placelocation = returned[0][2]
            if board.placing == 1:
                board.white |= placelocation
            else:
                board.black |= placelocation
            board.printboard()
            board.invertboard(placelocation)
            sleep(0.8)
            board.printboard()
            board.switch()
            if aiplacing >= 0:
                aiplacing = abs(aiplacing - 1)     
        else:
            board.switch()
            if board.abletoplace():
                print(placingcolor + ' cannot place anywhere')
                if aiplacing >= 0:
                    aiplacing = abs(aiplacing - 1)
            else:
                # placercount = bin(placerboard)[2:].count('1')
                # opponentcount = bin(opponentboard)[2:].count('1')
                # if placercount > opponentcount:
                #     if aiplacing == -1:
                #         print(f'{placingcolor} won!')
                #     elif aiplacing == 0:
                #         print('you won!')
                #     else:
                #         print('ai won!')
                # elif placercount < opponentcount:
                #     if aiplacing == -1:
                #         print(f'{opponentcolor} won!')
                #     elif aiplacing == 0:
                #         print('ai won!')
                #     else:
                #         print('you won!')
                # else:
                #     print('draw!')
                whitecount = bin(board.white)[2:].count('1')
                blackcount = bin(board.black)[2:].count('1')
                if whitecount < blackcount:
                    if aiplacing == -1:
                        print('○ won!')
                    elif (2 * aiplacing - 1) == board.placing:
                        print('ai won!')
                    else:
                        print('you won!')
                elif whitecount > blackcount:
                    if aiplacing == -1:
                        print('● won!')
                    elif (2 * aiplacing - 1) == board.placing:
                        print('you won!')
                    else:
                        print('ai won!')                            
                else:
                    print('draw!')
                return


def main():
    play()
if __name__ == '__main__':
    main()