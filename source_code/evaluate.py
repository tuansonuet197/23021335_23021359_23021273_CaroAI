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
        
        for i in range(length - 3):
            window4 = line[i:i+4]
            p4 = window4.count(p)
            o4 = window4.count(o)
            
            # Ưu tiên tuyệt đối thắng/thua ngay lập tức
            if p4 == 4: line_score += 100000
            elif o4 == 4: line_score -= 100000
            
        for i in range(length - 4):
            window5 = line[i:i+5]
            pc = window5.count(p)
            oc = window5.count(o)
            
            if pc > 0 and oc > 0: continue
            
            # Phân tích các thế cờ "mở" (Live) - CỰC KỲ QUAN TRỌNG
            if oc == 3:
                # Thế cờ người chơi có 3 quân mở 2 đầu (hoặc 1 đầu nhưng luật 4 quân là thắng)
                if window5[0] == 0 and window5[4] == 0:
                    line_score -= 30000 # Rất nguy hiểm (Live 3)
                else:
                    line_score -= 15000 # Dead 3
            elif pc == 3:
                if window5[0] == 0 and window5[4] == 0:
                    line_score += 20000
                else:
                    line_score += 10000
            elif oc == 2:
                # Chặn sớm bộ 2 của người chơi
                if window5[0] == 0 and window5[1] == 0 and window5[4] == 0:
                    line_score -= 5000 # Live 2 thoáng
                else:
                    line_score -= 2000
            elif pc == 2:
                line_score += 500
                
        return line_score

    @staticmethod
    def score_move_quick(board, r, c, p):
        """
        Sắp xếp nước đi (Move Ordering) cực mạnh.
        Mô phỏng đếm chuỗi (run length) trên các tia để nhận diện đe dọa lớn mà không cần make_move.
        """
        score = 0
        size = board.size
        grid = board.grid
        o = 1 if p == 2 else 2
        
        # 1. Điểm ưu tiên vị trí trung tâm (tie-breaker)
        center = size / 2.0
        score -= (abs(r - center) + abs(c - center)) * 0.1
        
        # 2. Quét 4 hướng để đếm chuỗi liên tục
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            p_run = 0
            o_run = 0
            
            for step in [1, -1]:
                # Đếm chuỗi quân mình
                nr, nc = r + step*dr, c + step*dc
                while 0 <= nr < size and 0 <= nc < size:
                    if grid[nr][nc] == p:
                        p_run += 1
                        nr += step*dr
                        nc += step*dc
                    else:
                        break
                        
                # Đếm chuỗi quân địch
                nr, nc = r + step*dr, c + step*dc
                while 0 <= nr < size and 0 <= nc < size:
                    if grid[nr][nc] == o:
                        o_run += 1
                        nr += step*dr
                        nc += step*dc
                    else:
                        break
            
            # Ưu tiên phòng thủ: chặn địch có chuỗi dài
            if o_run >= 3: score += 5000 # Địch có 3 quân -> BẮT BUỘC CHẶN
            elif o_run == 2: score += 500
            elif o_run == 1: score += 50
            
            # Ưu tiên tấn công: nối dài chuỗi quân ta
            if p_run >= 3: score += 4000
            elif p_run == 2: score += 400
            elif p_run == 1: score += 40
                    
        return score
