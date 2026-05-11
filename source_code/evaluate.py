class Evaluator:
    # Bộ chỉ số cố định để tránh tính toán lại mỗi lần
    lines_indices = None
    size = 0

    @classmethod
    def init_indices(cls, size):
        if cls.lines_indices is not None and cls.size == size:
            return
        cls.size = size
        cls.lines_indices = []
        # Hàng ngang
        for r in range(size):
            cls.lines_indices.append([(r, c) for c in range(size)])
        # Hàng dọc
        for c in range(size):
            cls.lines_indices.append([(r, c) for r in range(size)])
        # Chéo chính
        for d in range(-size + 1, size):
            diag = [(i, i - d) for i in range(size) if 0 <= i - d < size]
            if len(diag) >= 4: cls.lines_indices.append(diag)
        # Chéo phụ
        for d in range(2 * size - 1):
            diag = [(i, d - i) for i in range(size) if 0 <= d - i < size]
            if len(diag) >= 4: cls.lines_indices.append(diag)

def evaluate_state(board_obj):
    """
    Hàm đánh giá sử dụng kỹ thuật String Pattern Matching cực nhanh.
    """
    Evaluator.init_indices(board_obj.size)
    
    grid = board_obj.grid
    lines = []
    for indices in Evaluator.lines_indices:
        lines.append("".join(str(grid[r][c]) for r, c in indices))
    
    # Tính điểm cho cả hai bên
    score = 0
    # Điểm của máy (Player 2)
    score += evaluate_lines(lines, player='2', opponent='1')
    # PHÒNG THỦ CỰC GẮT: Nhân hệ số 1.5 để AI ưu tiên chặn người chơi hơn là tấn công
    score -= evaluate_lines(lines, player='1', opponent='2') * 1.5
    
    return score

def evaluate_lines(lines, player, opponent):
    p = player
    o = opponent
    e = '0' # Ô trống
    
    score = 0
    
    # Từ điển các "Thế cờ" 4 quân chuẩn
    patterns = {
        # ---- THẮNG LUÔN (Win) ----
        p*4: 10000000,
        
        # ---- LIVE 3 (3 quân mở 2 đầu) - Cực nguy hiểm ----
        e+p+p+p+e: 1000000,
        e+p+e+p+p+e: 800000, 
        e+p+p+e+p+e: 800000, 
        
        # ---- DEAD 3 / BROKEN 3 ----
        e+p+p+p+o: 100000,
        o+p+p+p+e: 100000,
        p+e+p+p: 100000,     
        p+p+e+p: 100000,
        p+e+e+p+p: 80000,
        p+p+e+e+p: 80000,
        p+e+p+e+p: 80000,
        
        # ---- LIVE 2 (2 quân mở 2 đầu) ----
        e+p+p+e: 5000,
        e+p+e+p+e: 5000,
        
        # ---- DEAD 2 ----
        e+p+p+o: 500,
        o+p+p+e: 500
    }
    
    for line in lines:
        # PADDING: Coi mép bàn cờ là quân địch
        padded_line = o + line + o
        
        for pat, val in patterns.items():
            score += padded_line.count(pat) * val
            
    return score
