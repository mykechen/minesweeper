import random
import re

# create a board object to represent minesweeper game
# used for functions "create board", "dig here", "render this game for this object"
class Board:
    def __init__(self, dim_size, num_bombs) -> None:
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # create game board
        self.board = self.make_new_board()
        self.assign_values_to_board()

        # initialize set to keep track of dug locations
        # save (row, col) tuples into this set
        self.dug = set()

    def make_new_board(self):
        # construct a new board based on dim size and num bombs
        # 2D list

        # generates an empty dim_size x dim_size board 
        # [[None, None, etc.]]
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        # places bombs randomly
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            row = random.randint(0, self.dim_size - 1)
            col = random.randint(0, self.dim_size - 1)

            if board[row][col] == '*':
                continue

            board[row][col] = '*'
            bombs_planted += 1

        return board
    
    # assigns values to each spot on board based on how many bombs nearby (0-8)
    def assign_values_to_board(self):
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                # continue if spot is bomb
                if self.board == '*':
                    continue
                self.board[row][col] = self.get_num_neighboring_bombs(row, col)

    def get_num_neighboring_bombs(self, row, col):
        num_neighboring_bombs = 0
        
        for r in range(max(0, row-1), min(row+1, self.dim_size - 1) + 1):
            for c in range(max(0, col-1), min(self.dim_size - 1, col+1) + 1):
                # reduce this bottom code in the for loop
                # if r < 0 or r >= self.dim_size or c < 0 or c >= self.dim_size:
                #     continue
                if r == row and c == col:
                    continue
                else:
                    if self.board[r][c] == '*':
                        num_neighboring_bombs += 1

        return num_neighboring_bombs
    
    def dig(self, row, col):
        # dig at row, col
        # return True if successful dig, False if bomb dug

        # 3 scenarios: dug bomb, dug with neighboring bombs, dug with no neighboring bombs

        # keep track where we dug
        self.dug.add((row, col))

        # base cases
        if self.board[row][col] == '*':
            print("Bomb here in dig")
            return False
        # stops mining if neighboring a bomb
        # base case for recursion
        elif self.board[row][col] > 0:
            print("Bomb nearby in dig")
            return True
        
        # recursion if self.board[row][col] == 0
        for r in range(max(0, row - 1), min(row + 1, self.dim_size - 1) + 1):
            for c in range(max(0, col - 1), min(col + 1, self.dim_size - 1) + 1):
                if (r, c) in self.dug:
                    continue # don't dig where you have already dug
                print("In recursion dig")
                self.dig(r, c)

        return True
    
    def __str__(self) -> str:
        # call with print function to display the board

        # initialize visible board array, what the user will see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        
        # print visible board
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep

def play(dim_size=10, num_bombs=10):
    # step 1: create the board and plant the bombs
    board = Board(dim_size, num_bombs)

    # step 2: display the board and ask user where to dig
    # step 3a: if location is a bomb, show game over message
    # step 3b: if location is not a bomb, dig recursively until each square is at least next to a bomb
    # step 4: repeat steps 2 and 3a/b until there are no more places to dig -> WIN!

    safe = True
    print("Is it safe? ", safe)
    while len(board.dug) < board.dim_size**2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row, col: "))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= dim_size or col < 0 or col >= dim_size:
            print("Invalid location. Try again.")
            continue

        # check if dig is safe
        safe = board.dig(row, col)
        print(f'Row: {row}, Col: {col}')
        # print("Inside of while loop and Safe = ")
        print("Safe: ")
        if not safe:
            # dug a bomb
            break
    
    print("Outside of while loop")
    # 2 ways to end loop, dug all spots or hit bomb
    if safe:
        print("You have dug all locations. You WON!")
    else:
        print("You dug a bomb. You LOSE")
        # reveal the board
        board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

# good practice
if __name__ == '__main__':
    play()