
import random

# Connect Four against a human or an AI with 5 levels of difficulty. Have fun!

class Board:
    """A data type representing a Connect-4 board
       with an arbitrary number of rows and columns.
    """
    
    def __init__(self, width, height):
        """Construct objects of type Board, with the given width and height.
        """
        self.width = width
        self.height = height
        self.data = [[' ']*width for row in range(height)]

    def __repr__(self):
        """This method returns a string representation
           for an object of type Board.
        """
        s = ''                          # the string to return
        for row in range(0, self.height):
            s += '|'
            for col in range(0, self.width):
                s += self.data[row][col] + '|'
            s += '\n'

        s += (2*self.width + 1) * '-'   # bottom of the board

        # and the numbers underneath here

        return s       # the board is complete, return it

    def addMove(self, col, ox):
        """Drops a checker into the board
           argument col: column
           argument ox: what type of marker ('X' or 'O')
        """
        for row in range(0, self.height):
            if self.data[row][col] != ' ':
                self.data[row-1][col] = ox
                return

        # if col==4:
        #     print("Should not be here!")
        #     print(self) 
        self.data[self.height-1][col] = ox
    
    def clear(self):
        """clears board
        """
        for row in range(0, self.height):
            for col in range(0, self.width):
                self.data[row][col] = ' '


    def setBoard(self, moveString):
        """Accepts a string of columns and places
           alternating checkers in those columns,
           starting with 'X'.

           For example, call self.setBoard('012345')
           to see 'X's and 'O's alternate on the
           bottom row, or self.setBoard('000000') to
           see them alternate in the left column.

           moveString must be a string of one-digit integers.
        """
        nextChecker = 'X'   # start by playing 'X'
        for colChar in moveString:
            col = int(colChar)
            if 0 <= col <= self.width:
                self.addMove(col, nextChecker)
            if nextChecker == 'X':
                nextChecker = 'O'
            else:
                nextChecker = 'X'
    def allowsMove(self, c):
        """checks to see if a move is allowed
           Returns True or False
           argument c: column
        """
        if c not in range(0,self.width):
            return False
        elif self.data[0][c] != ' ':
            return False
        else: return True
    def isFull(self):
        """checks if the board is full
        """
        for row in range(0, self.height):
            for col in range(0, self.width):
                if self.data[row][col] == ' ':
                    return False
        return True

    def delMove(self, c):
        """removes top checker from column c
        """
        for row in range(0, self.height):
            if self.data[row][c] != ' ':
                self.data[row][c] = ' '
                return
    def winsFor(self, ox):
        """returns true if four ox checkers exist in a row
        """
        for row in range(0, self.height):
            for col in range(0, self.width - 3):
                if self.data[row][col] == ox and \
                   self.data[row][col + 1] == ox and \
                   self.data[row][col + 2] == ox and \
                   self.data[row][col + 3] == ox:
                    return True
        for row in range(0, self.height-3):
            for col in range(0, self.width):
                if self.data[row][col] == ox and \
                   self.data[row+1][col] == ox and \
                   self.data[row+2][col] == ox and \
                   self.data[row+3][col] == ox:
                    return True
        for row in range(0, self.height-3):
            for col in range(0, self.width - 3):
                if self.data[row][col] == ox and \
                   self.data[row+1][col+1] == ox and \
                   self.data[row+2][col+2] == ox and \
                   self.data[row+3][col+3] == ox:
                    return True
        for row in range(3, self.height):
            for col in range(0, self.width - 3):
                if self.data[row][col] == ox and \
                   self.data[row-1][col+1] == ox and \
                   self.data[row-2][col+2] == ox and \
                   self.data[row-3][col+3] == ox:
                    return True
        return False

    def colsToWin(self, ox):
        """returns a list of columns where argument ox can win
           ox: 'X' or 'O'
        """
        compiler = []
        for i in range(self.width):
            if self.allowsMove(i) == True:
                self.addMove(i, ox)
                if self.winsFor(ox) == True:
                    compiler += [i]
                    self.delMove(i)
                else: self.delMove(i)
        return compiler

    def aiMove(self, ox):
        """returns a winning move
           if impossible returns a move to prevent opponents winning move
           if impossible moves in the leftmost possible column
        """
        colwin = self.colsToWin(ox)
        colwinO = self.colsToWin('O')
        colwinX = self.colsToWin('X')
        if len(colwin) != 0:
            self.addMove((colwin[0]), ox)
            return int(colwin[0])
        elif ox == 'X' and self.colsToWin('O') != []:
            self.addMove((colwinO[0]), ox)
            return int(colwinO[0])
        elif ox == 'O' and self.colsToWin('X') != []:
            self.addMove((colwinX[0]), ox)
            return int(colwinX[0])
        else:
            for i in range(self.width):
                if self.allowsMove(i) == True:
                    self.addMove(i, ox)
                    return i
                else: return

    def hostHumGame(self):
        """host human v human game"""
        print("The Connect Four showdown begins!")
        while True:
            users_col = -1
            while not self.allowsMove(users_col):
                print(self)
                print(" 0 1 2 3 4 5 6")
                print("X's turn.")
                users_col = int(input("Choose a column: "))
                self.addMove(users_col,'X')
            if self.winsFor('X') == True:
                break
            if self.isFull() == True:
                print("Full board, tie game!")
                break
            
            users_col = -1
            while not self.allowsMove(users_col):
                print(self)
                print(" 0 1 2 3 4 5 6")
                print("O's turn.")
                users_col = int(input("Choose a column: "))
                self.addMove(users_col,'O')
            if self.winsFor('O') == True:
                break
            if self.isFull() == True:
                print ("Full board, tie game!")
                break    
        if self.winsFor('X') == True:
            print(self)
            print('X wins! Yay!')
        if self.winsFor('O') == True:
            print(self)
            print('O wins! Yay!')

    def playGame(self):
        """Plays a game of connect 4 between two player objects
           argument px and po: two player objects
        """
        print("Let's play some Connect Four!")
        userxo = input("Would you like X, or O? Enter a lower case character.\n")
        if userxo == "x":
            px = 'h'
            po = input("\nPlaying a human, or a computer?\nEnter 'h' for human or 'c' for computer.\n")
            if po == 'c':
                temp = input("\nSelect AI difficulty. \nEnter 0, 1, 2, 3, or 4.\n")
                po = Player("X", "RANDOM", int(temp))
        if userxo == "o":
            po = 'h'
            px = input("Playing a human, or a computer?\nEnter 'h' for human or 'c' for computer.\n")
            if px == 'c':
                temp = input("\nSelect AI difficulty. \nEnter 0, 1, 2, 3, or 4.\n")
                px = Player("X", "RANDOM", int(temp))
        if px == 'h':
            if po == 'h':
                self.hostHumGame()    #both human
            else:
                print("The Connect Four showdown begins!")
                print("You've chosen 'X'.")
                while True:
                    users_col = -1
                    while not self.allowsMove(users_col):
                        print(self)
                        print(" 0 1 2 3 4 5 6")
                        print("Your turn!")
                        users_col = int(input("Choose a column: "))
                        self.addMove(users_col,'X')
                        print(self)
                    if self.winsFor('X') == True:
                        break
                    if self.isFull() == True:
                        print("Full board, tie game!")
                        break
                    self.addMove(po.nextMove(self), 'O')
                    if self.winsFor('O') == True:
                        break
                    if self.isFull() == True:
                        print(self)
                        print("Full board, tie game!")
                        break
                    
                if self.winsFor('X') == True:
                    print('You win! Congrats!')
                if self.winsFor('O') == True:
                    print(self)
                    print('I win! But more importantly, you lose! HAHAHA')
        elif po == 'h' and px != 'h':               #o human x computer
            print("The Connect Four showdown begins!")
            print("You've chosen 'O'.")
            while True:
                users_col = -1
                self.addMove(px.nextMove(self), 'X')
                if self.winsFor('X') == True:
                    break
                if self.isFull() == True:
                    print(self)
                    print("Full board, tie game!")
                    break
                while not self.allowsMove(users_col):
                    print(self)
                    print(" 0 1 2 3 4 5 6")
                    print("Your turn!")
                    users_col = int(input("Choose a column: "))
                    self.addMove(users_col,'O')
                    print(self)
                if self.winsFor('O') == True:
                    break
                if self.isFull() == True:
                    print("Full board, tie game!")
                    break
            if self.winsFor('O') == True:
                print('You win! Congrats!')
            if self.winsFor('X') == True:
                print(self)
                print('I win! But more importantly, you lose! HAHAHA')
        else:                         #x human o computer
            while True:
                self.addMove(px.nextMove(self), 'X')
                
                if self.winsFor('X') == True:
                    break
                if self.isFull() == True:
                    print(self)
                    print("Full board, tie game!")
                    break
                print(self)
                self.addMove(po.nextMove(self), 'O')

                if self.winsFor('O') == True:
                    break
                if self.isFull() == True:
                    print(self)
                    print("Full board, tie game!")
                    break
                print(self)
            if self.winsFor('O') == True:
                print(self)
                print("O wins!" )
            if self.winsFor('X') == True:
                print(self)
                print('X wins!')


class Player:
    """An AI player for Connect Four."""

    def __init__(self, ox, tbt, ply):
        """Construct a player for a given checker, tie-breaking type,
           and ply."""
        self.ox = ox
        self.tbt = tbt
        self.ply = ply

    def __repr__(self):
        """Create a string represenation of the player."""
        s = "Player for " + self.ox + "\n"
        s += "  with tiebreak type: " + self.tbt + "\n"
        s += "  and ply == " + str(self.ply) + "\n\n"
        return s
    
    def oppCh(self):
        """returns the opposite character of self (X and O)"""
        if self.ox == 'X':
            return 'O'
        if self.ox == 'O':
            return 'X'

    def scoreBoard(self, b):
        """returns float representing winning chances of self"""
        if b.winsFor(self.ox) == True:
            return 100.0
        elif b.winsFor(self.oppCh()) == True:
            return 0.0
        else: return 50.0

    def tiebreakMove(self, scores):
        """takes in scores from scoreboard and returns the ideal column
           if there is only one best move. If there's a tie, it is broken using
           the keywords 'LEFT' (leftmost best move), 'RIGHT' (rightmost best move),
           or 'RANDOM' which returns a randombest option
        """       
        L = []
        N = 0
        for i in scores:
            if i == max(scores):
                L += [N]
            N+=1
        if len(L) > 1:
            if self.tbt == 'LEFT':
                return L[0]
            elif self.tbt == 'RIGHT':
                return L[-1]
            elif self.tbt == 'RANDOM':
                return random.choice(L)
        elif L == [0]*b.width:
            L = b.winsFor(self.oppCh)
            if self.tbt == 'LEFT':
                return L[0]
            elif self.tbt == 'RIGHT':
                return L[-1]
            elif self.tbt == 'RANDOM':
                return random.choice(L)
        else: return L[0]
            
    def scoresFor(self, b):
        """return a list of scores, with the cth score 
           representing the "goodness" of the input board after the 
           player moves to column c.
           argument b: board
        """
        
        L = [50]*b.width
        for i in range(0, b.width):
            if b.allowsMove(i) == False:
                L[i] = -1.0
            elif b.winsFor(self.ox) == True:
                L[i] = 100
            elif b.winsFor(self.oppCh()) == True:
                L[i] = 0
            elif self.ply == 0:
                L[i] = 50
            elif self.ply > 0:
                b.addMove(i, self.ox)
                op = Player(self.oppCh(), self.tbt, self.ply-1)
                opScores = op.scoresFor(b)
                L[i] = 100-max(opScores)
                b.delMove(i)
        return L

    def nextMove(self, b):
        """accepts object of type board (b)
           returns column number column object chooses to move to
        """
        return self.tiebreakMove(self.scoresFor(b))

b = Board(7,6)
b.playGame()