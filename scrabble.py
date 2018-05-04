import sys
from unionfind import UF
# The board is stored in board. Grows down and right.
# board[i][j] is row i and column j

board = [] # current stat of the board
letters = set() # letter i can play
wordsOfLength = [] # set of all words of lengths 1, 2... 7
dict = set() # the dictionary

def makeWords():
    for n in range(1, 8):
        wordsOfLength.append(stringsOfLength(n, letters))


def isWord(word):
    return word in dict


def printBoard(tboard):
    '''
        Prints the board nicely.
    '''
    out = ''
    row = 0
    while row < 15:
        start = 0
        end = 0
        while True:
            # there many be may words in a row
            while start < 15 and tboard[row][start] == '':
                start += 1
                out += ' '

            if start < 14:
                #print('Found a word in row %d.' % row)
                # there is something to check. If single letter, then
                # need only check vertically.
                end = start
                while end < 14 and tboard[row][end+1] != '': end += 1

                # know the start and end of the string. Check if word.
                #print('Found end at end = %d.' % end)
                if start < end:
                    # make the string
                    s = ''
                    for i in range(start, end + 1):
                        s += tboard[row][i]
                    out += s
                else:
                    out += tboard[row][start]
                start = end + 1 # move to next empty space

            if start >= 14: break

        # move to next row
        row += 1
        out += '\n'

    print(out)


def testBoardHorizontally(tboard, horiz, clusters):
    '''
        Test if this board has only valid words.
        Do this by walking right through each row looking for string separated
        by spaces. Check each.
    '''


    row = 0
    while row < 15:
        start = 0
        end = 0

        while True:
            # there many be may words in a row
            while start < 15 and tboard[row][start] == '':
                start += 1

            if start < 14:
                #print('Found a word in row %d.' % row)
                # there is something to check. If single letter, then
                # need only check vertically.
                end = start
                while end < 14 and tboard[row][end+1] != '': end += 1
                # know the start and end of the string. Check if word.
                #print('Found end at end = %d.' % end)
                if start < end:
                    # make the string
                    s = ''
                    for i in range(start, end + 1):
                        s += tboard[row][i]
                        if i > start:
                            if horiz:
                                clusters.union(15 * row + i-1, 15 * row + i)
                            else:
                                clusters.union(15 *(i-1) + row, 15 *i + row)
                    if not isWord(s): return False
                start = end + 1 # move to next empty space

            if start >= 14: break

        # move to next row
        row += 1

    return True


def validBoard(tboard):
    clusters = UF(15 * 15) # created a Union-Find datastructure for connectedness of words
    if not testBoardHorizontally(tboard, True, clusters): return False
    if not testBoardHorizontally(transpose(tboard), False, clusters): return False

    '''
        Now check connectedness. The number of clusters should equal 15^2 - number
        of letters on the board.
    '''

    numLetters = 0
    for i in range(15):
        for j in range(15):
            if tboard[i][j] != '': numLetters += 1

    return clusters.numClusters() == 1 +  15*15 - numLetters


def stringsOfLength(n, letters):
    '''
        Give me all the strings of length n made of "letters" using
        each only once.
    '''

    if n == 1:
        # base case
        return letters
    else:
        res = set()
        for char in letters:
            sublst = stringsOfLength(n-1, letters.difference({char}))
            for word in sublst:
                 res.add(char + word)
        return res

def addString(i, j, word, brd):
    # deepcopy
    newboard = [[brd[row][col] for col in range(15)] for row in range(15)]

    row = i
    col = j
    counter = 0

    while col < 15 and counter < len(word):
        if brd[row][col] == '':
            # add letter
            w = word[counter]
            newboard[row][col] = w
            counter +=1
        col += 1 # if not empty then just skip

    return newboard

def transpose(brd):
    return [[brd[j][i] for j in range(15)] for i in range(15)]


def getMoves():
    '''
        Fill in words in all possible ways. Then test which are valid placements.
    '''

    moves = []
    transposed_board = transpose(board)


    for i in range(15):
        #print('Checking row %d' % i)
        for j in range(15):
            #print('Checking col %d' % j)
            if board[i][j] == '':
                # this cell is empty so can start placing letters here
                for n in range(1, 8):
                    # iterate over placements of 1..7 letters
                    for word in wordsOfLength[n-1]:
                        # place horizontally
                        testboard = addString(i, j, word, board)
                        if testboard != None:
                            # was able to place this string without running
                            # off or overwritting existing letters
                            if validBoard(testboard):
                                moves.append((i,j,word,'h'))
                                printBoard(testboard)


    # Now try adding words horizontally into the transposed board.
    # This is equivalent to adding vertically into original board.
    for i in range(15):
        for j in range(15):
            if transposed_board[i][j] == '':
                # this cell is empty so can start placing letters here
                for n in range(1, 8):
                    # iterate over placements of 1..7 letters
                    for word in wordsOfLength[n-1]:
                        # place horizontally
                        testboard = addString(i, j, word, transposed_board)
                        if testboard != None:
                            # was able to place this string without running
                            # off or overwritting existing letters
                            if validBoard(testboard):
                                moves.append((i,j,word,'v'))
                                printBoard(transpose(testboard))


    return moves


boardfile = open(sys.argv[1],'r')
lettersfile = open(sys.argv[2],'r')
dictfile = open(sys.argv[3], 'r')

board = [['' for col in range(15)] for row in range(15)] # current stat of the board

for line in boardfile.readlines():
    row, col, char  = line.split()
    row = int(row)
    col = int(col)
    board[row][col] = char.upper()

print(board)


for line in lettersfile.readlines():
    for char in line.split():
        letters.add(char.upper())
print(letters)

counter = 0
for line in dictfile.readlines():
    dict.add(line.split()[0])
    if counter > 10:
        print('AA' in dict)
        sys.exit(0)

print(len(dict))
print('CAR' in dict)

makeWords()
moves = getMoves()

for move in moves:
    if move[3] == 'v':
        dir = 'vertically'
    else:
        dir = 'horizontally'
    print('%s at (row,col) = (%d, %d) %s' % (move[2], move[0], move[1], dir))
