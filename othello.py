
import alphabeta
from bitboard import Othelloboard
import testcase
from time import sleep, time


def validinput(ask, wrong, *valids):
    while True:
        inputted = input(ask)
        if inputted not in set(valids):
            print(wrong)
            sleep(0.8)
        else:
            break
    return inputted



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
    
    board = testcase.BEST_WHITE_15_LEFT

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
                    start = time()
                    returned = alphabeta.best_locations_list(board)
                    print(time() - start)
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
                returned = alphabeta.best_locations_list(board)
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