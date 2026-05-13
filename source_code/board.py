class Board:
    def __init__(self, size=9):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.move_history = []
        self.move_count = 0

    def copy(self):
        """Tạo bản sao lưu bàn cờ."""
        new_board = Board(self.size)
        new_board.grid = [row[:] for row in self.grid]
        new_board.move_history = self.move_history[:]
        new_board.move_count = self.move_count
        return new_board

    @property
    def last_move(self):
        if not self.move_history:
            return None
        return self.move_history[-1][0], self.move_history[-1][1]

    def is_valid_move(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c] == 0

    def make_move(self, r, c, player):
        if self.is_valid_move(r, c):
            self.grid[r][c] = player
            self.move_history.append((r, c, player))
            self.move_count += 1
            return True
        return False
    
    def undo_move(self, r, c, player):
        if self.move_history:
            last_r, last_c, last_p = self.move_history.pop()
            self.grid[last_r][last_c] = 0
            self.move_count -= 1

    def get_valid_moves(self, search_radius=2):
        """
        Gợi ý cải tiến: Chỉ sinh các nước đi gần những quân đã đánh.
        Nếu bàn cờ trống, đánh vào tâm.
        """
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
        """Kiểm tra xem đã có ai thắng chưa (đủ 4 quân liên tiếp)."""
        lm = self.last_move
        if not lm: return None
        r, c = lm
        player = self.grid[r][c]
        
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
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
            return 0 # Hòa
        return None
