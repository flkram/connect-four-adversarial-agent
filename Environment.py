import numpy as np
from enum import Enum

class Status(Enum):
    BLANK = ' '
    RED = 'R'
    YELLOW = 'Y'
    DRAW = 'D'
    ONGOING = 'O'

class Environment:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.board = np.full((self.rows, self.cols), Status.BLANK)
        self.current_player = Status.YELLOW 
        self.game_status = Status.ONGOING
        
    def get_valid_moves(self):
        return [col for col in range(self.cols) if self.board[0][col] == Status.BLANK]
    
    def drop_piece(self, col):
        if col not in self.get_valid_moves():
            return False
            
        for row in reversed(range(self.rows)):
            if self.board[row][col] == Status.BLANK:
                self.board[row][col] = self.current_player
                self._check_game_status(row, col)
                self._switch_player()
                return True
        return False
    
    def _switch_player(self):
        self.current_player = Status.YELLOW if self.current_player == Status.RED else Status.RED
    
    def _check_game_status(self, row, col):
        player = self.board[row][col]
        
        directions = [
            (0, 1),  # Horizontal
            (1, 0),  # Vertical
            (1, 1),  # Diagonal down-right
            (1, -1)  # Diagonal down-left
        ]
        
        for dr, dc in directions:
            count = 1
            for i in [1, -1]:
                r, c = row + dr*i, col + dc*i
                while 0 <= r < self.rows and 0 <= c < self.cols:
                    if self.board[r][c] == player:
                        count += 1
                        r += dr*i
                        c += dc*i
                    else:
                        break
            if count >= 4:
                self.game_status = player
                return
                
        if len(self.get_valid_moves()) == 0:
            self.game_status = Status.DRAW
            
    def clone(self):
        cloned = Environment()
        cloned.board = np.copy(self.board)
        cloned.current_player = self.current_player
        cloned.game_status = self.game_status
        return cloned
    
    def print_board(self):
        print("\n".join(["|" + "|".join([cell.value for cell in row]) + "|" for row in self.board]))
        print("-" * (self.cols * 2 + 1))