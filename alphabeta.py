from bitboard import Othelloboard

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
            winner_color = temp.get_winner()
            #self 1 placing 1 - placing white, my turn - i am white
            #self 1 placing -1  - placing black, my turn - i am black
            #self -1 placing 1 - placing white, opponent turn - i am black
            #self -1 placing -1  - placing black, opponent turn - i am white
            if winner_color == 0:
                return (0, 1)
            elif self * -temp.placing == 1:
                #input('winreturn')
                if winner_color == 1:
                    return (1, 1)
                else:
                    return (-1, 1)
            else:
                if winner_color == 1:
                    return (-1, 1)
                else:
                    return (1, 1)
                
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


def best_locations_list(board:Othelloboard):
    returninglist = []
    possiblelocation = board.abletoplace()
    onlylocation = 1
    while possiblelocation != 0:
        if possiblelocation & 1 != 0:
            temp = Othelloboard(board.white, board.black, board.placing)
            temp.invertboard(onlylocation)
            temp.switch()
            value = findextreme(temp, (-1, 0), (1, 0), -1)
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
