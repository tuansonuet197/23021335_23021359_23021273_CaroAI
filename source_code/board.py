import random

class Board:
    def __init__(self, size=9):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.last_move = None
        self.move_count = 0

    def is_valid_move(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c] == 0

    def make_move(self, r, c, player):
        if self.is_valid_move(r, c):
            self.grid[r][c] = player
            self.last_move = (r, c)
            self.move_count += 1
            return True
        return False
    
    def undo_move(self, r, c, player):
        self.grid[r][c] = 0
        self.move_count -= 1

    def get_valid_moves(self, search_radius=1):
        if self.move_count == 0:
            return [(self.size // 2, self.size // 2)]
        moves = set()
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != 0:
                    for i in range(-search_radius, search_radius + 1):
                        for j in range(-search_radius, search_radius + 1):
                            nr, nc = r + i, c + j
                            if 0 <= nr < self.size and 0 <= nc < self.size and self.grid[nr][nc] == 0:
                                moves.add((nr, nc))
        return list(moves)

    def check_winner(self, win_count=4):
        if not self.last_move: return None
        r, c = self.last_move
        player = self.grid[r][c]
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            count = 1
            # Kiểm tra 2 phía của nước đi cuối cùng
            for direction in [1, -1]:
                for step in range(1, win_count):
                    nr, nc = r + dr * step * direction, c + dc * step * direction
                    if 0 <= nr < self.size and 0 <= nc < self.size and self.grid[nr][nc] == player:
                        count += 1
                    else:
                        break
            if count >= win_count:
                return player
                
        if self.move_count == self.size * self.size:
            return 0
        return None
