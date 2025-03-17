from Environment import Status
import random

class Robot:
    def get_action(self, env):
        raise NotImplementedError

class StudentRobot(Robot):
    def get_action(self, env):
        valid_moves = env.get_valid_moves()
        
        # Check for immediate win
        for move in valid_moves:
            cloned = env.clone()
            if cloned.drop_piece(move) and cloned.game_status == env.current_player:
                return move
                
        # Block opponent win
        opponent = Status.YELLOW if env.current_player == Status.RED else Status.RED
        for move in valid_moves:
            cloned = env.clone()
            cloned.current_player = opponent
            if cloned.drop_piece(move) and cloned.game_status == opponent:
                return move
                
        # Minimax with alpha-beta pruning
        _, best_move = self.minimax(env.clone(), depth=4, alpha=-float('inf'), beta=float('inf'), maximizing=True)
        return best_move or random.choice(valid_moves)
    
    def minimax(self, env, depth, alpha, beta, maximizing):
        if depth == 0 or env.game_status != Status.ONGOING:
            return 0, None
            
        valid_moves = env.get_valid_moves()
        best_value = -float('inf') if maximizing else float('inf')
        best_move = None
        
        for move in valid_moves:
            cloned = env.clone()
            cloned.drop_piece(move)
            
            if maximizing:
                value, _ = self.minimax(cloned, depth-1, alpha, beta, False)
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, best_value)
            else:
                value, _ = self.minimax(cloned, depth-1, alpha, beta, True)
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, best_value)
            
            if alpha >= beta:
                break
                
        return best_value, best_move
    
    def evaluate(self, env):
        # Immediate win/loss/draw detection
        if env[env.game_status] == self:
            return 10000
        if env.game_status != Status.ONGOING:
            return -10000 if env.game_status != Status.DRAW else 0

        score = 0
        opponent = Status.YELLOW if self.role == Status.RED else Status.RED
        
        # Potential line evaluation
        for target, weight in [(3, 100), (2, 10), (1, 1)]:
            player_pot = self._count_potential(env.board, self.role, target)
            opp_pot = self._count_potential(env.board, opponent, target)
            score += player_pot * weight
            score -= opp_pot * weight

        # Center control bonus (columns 2, 3, 4)
        for row in range(env.rows):
            for col in [2, 3, 4]:
                if env.board[row][col] == self.role:
                    score += 2
                    
        return score

    def _count_potential(self, board, player, target):
        count = 0
        rows, cols = board.shape
        
        # Horizontal
        for r in range(rows):
            for c in range(cols - 3):
                line = [board[r][c+i] for i in range(4)]
                p_count = sum(1 for cell in line if cell == player)
                blanks = sum(1 for cell in line if cell == Status.BLANK)
                if p_count + blanks == 4 and p_count == target:
                    count += 1

        # Vertical
        for c in range(cols):
            for r in range(rows - 3):
                line = [board[r+i][c] for i in range(4)]
                p_count = sum(1 for cell in line if cell == player)
                blanks = sum(1 for cell in line if cell == Status.BLANK)
                if p_count + blanks == 4 and p_count == target:
                    count += 1

        # Diagonal (down-right)
        for r in range(rows - 3):
            for c in range(cols - 3):
                line = [board[r+i][c+i] for i in range(4)]
                p_count = sum(1 for cell in line if cell == player)
                blanks = sum(1 for cell in line if cell == Status.BLANK)
                if p_count + blanks == 4 and p_count == target:
                    count += 1

        # Diagonal (up-right)
        for r in range(3, rows):
            for c in range(cols - 3):
                line = [board[r-i][c+i] for i in range(4)]
                p_count = sum(1 for cell in line if cell == player)
                blanks = sum(1 for cell in line if cell == Status.BLANK)
                if p_count + blanks == 4 and p_count == target:
                    count += 1

        return count

class RandomRobot(Robot):
    def get_action(self, env):
        return random.choice(env.get_valid_moves())