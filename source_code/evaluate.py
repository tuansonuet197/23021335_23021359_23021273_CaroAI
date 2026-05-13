class Evaluator:
    @staticmethod
    def evaluate_state(board_obj, ai_player=2):
        size = board_obj.size
        grid = board_obj.grid
        human_player = 1 if ai_player == 2 else 2
        
        score = 0
        # Hàng ngang
        for r in range(size):
            score += Evaluator.evaluate_line(grid[r], ai_player, human_player)
        # Hàng dọc
        for c in range(size):
            line = [grid[r][c] for r in range(size)]
            score += Evaluator.evaluate_line(line, ai_player, human_player)
        # Chéo chính
        for d in range(-size + 1, size):
            line = [grid[i][i - d] for i in range(size) if 0 <= i - d < size]
            if len(line) >= 4:
                score += Evaluator.evaluate_line(line, ai_player, human_player)
        # Chéo phụ
        for d in range(2 * size - 1):
            line = [grid[i][d - i] for i in range(size) if 0 <= d - i < size]
            if len(line) >= 4:
                score += Evaluator.evaluate_line(line, ai_player, human_player)
        return score

    @staticmethod
    def evaluate_line(line, p, o):
        line_score = 0
        length = len(line)
        
        # Cửa sổ 4 ô để phát hiện thắng thua ngay lập tức
        for i in range(length - 3):
            window4 = line[i:i+4]
            p4 = window4.count(p)
            o4 = window4.count(o)
            if p4 == 4: line_score += 100000
            elif o4 == 4: line_score -= 100000
            
        # Cửa sổ 5 ô để phát hiện thế trận Live 2, Live 3 (Quan trọng cho chặn chéo)
        for i in range(length - 4):
            window5 = line[i:i+5]
            pc = window5.count(p)
            oc = window5.count(o)
            
            if pc > 0 and oc > 0: continue
            
            # Ưu tiên phòng thủ cực cao cho các thế cờ "mở"
            if oc == 3:
                if window5[0] == 0 and window5[4] == 0: line_score -= 20000 # Live 3 của người
                else: line_score -= 10000 # Dead 3
            elif pc == 3:
                if window5[0] == 0 and window5[4] == 0: line_score += 8000 # Live 3 của máy
                else: line_score += 5000
            elif oc == 2:
                if window5[0] == 0 and window5[4] == 0: line_score -= 2000 # Live 2 của người (Phải chặn sớm!)
                else: line_score -= 500
            elif pc == 2:
                line_score += 100
                
        return line_score

    @staticmethod
    def score_move_quick(board, r, c, p):
        """
        Đánh giá nhanh để sắp xếp nước đi. 
        Cải tiến: Cộng điểm lớn cho việc chặn đứng các chuỗi quân của địch.
        """
        score = 0
        size = board.size
        grid = board.grid
        o = 1 if p == 2 else 2
        
        # Gần tâm
        center = size // 2
        score += (center - abs(r - center) - abs(c - center))
        
        # Xét 4 hướng để tìm quân địch xung quanh
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            for step in [1, -1]:
                nr, nc = r + dr * step, c + dc * step
                if 0 <= nr < size and 0 <= nc < size:
                    val = grid[nr][nc]
                    if val == o: score += 50 # Ưu tiên chặn địch
                    elif val == p: score += 30 # Ưu tiên nối quân mình
        return score
