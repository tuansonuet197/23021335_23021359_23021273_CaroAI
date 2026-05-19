import time
from evaluate import Evaluator

class AI:
    def __init__(self):
        self.states_evaluated = 0
        self.ai_player = 2
        self.human_player = 1
        # Bảng băm đơn giản để lưu trữ các trạng thái đã tính (Transposition Table)
        # Giúp AI không phải tính lại các nhánh trùng lặp
        self.memo = {}

    def get_best_move(self, board, max_depth, use_alpha_beta=True, ai_player=2):
        self.states_evaluated = 0
        self.ai_player = ai_player
        self.human_player = 1 if ai_player == 2 else 2
        self.memo = {} # Xóa bộ nhớ đệm mỗi lượt đi
        
        start_time = time.time()
        
        # 1. KIỂM TRA PHẢN XẠ NHANH (Nước đi bắt buộc)
        # Nếu có thể thắng ngay hoặc phải chặn đối thủ thắng ngay -> Đi luôn
        forced = self.find_forced_move(board)
        if forced:
            return forced, 100000, 1, time.time() - start_time

        # 2. TÌM KIẾM CHIẾN THUẬT
        best_move = None
        best_score = -float('inf')
        
        # Kỹ thuật Iterative Deepening: Tìm sâu dần từ 1 đến max_depth
        # Giúp AI có nước đi "khá" ngay cả khi bị hết thời gian
        for current_depth in range(1, max_depth + 1):
            if use_alpha_beta:
                score, move = self.alpha_beta_search(board, current_depth, -float('inf'), float('inf'), True)
            else:
                score, move = self.minimax_search(board, current_depth, True)
            
            if move:
                best_move = move
                best_score = score
            
            # Nếu đã tốn hơn 2 giây, không tìm sâu hơn nữa để tránh treo máy
            if time.time() - start_time > 2.0:
                break
                
        execution_time = time.time() - start_time
        return best_move, best_score, self.states_evaluated, execution_time

    def find_forced_move(self, board):
        """Tìm nước đi thắng ngay hoặc chặn đối phương thắng ngay."""
        valid_moves = board.get_valid_moves(search_radius=2)
        # Ưu tiên thắng trước
        for r, c in valid_moves:
            if board.make_move(r, c, self.ai_player):
                if board.check_winner(win_count=4) == self.ai_player:
                    board.undo_move(r, c, self.ai_player)
                    return (r, c)
                board.undo_move(r, c, self.ai_player)
        # Sau đó mới đến chặn
        for r, c in valid_moves:
            if board.make_move(r, c, self.human_player):
                if board.check_winner(win_count=4) == self.human_player:
                    board.undo_move(r, c, self.human_player)
                    return (r, c)
                board.undo_move(r, c, self.human_player)
        return None

    def minimax_search(self, board, depth, is_maximizing):
        self.states_evaluated += 1
        winner = board.check_winner(win_count=4)
        if winner is not None:
            if winner == self.ai_player: return 100000 + depth, None
            if winner == self.human_player: return -100000 - depth, None
            return 0, None
        if depth == 0:
            return Evaluator.evaluate_state(board, self.ai_player), None

        valid_moves = board.get_valid_moves(search_radius=2)
        if not valid_moves: return Evaluator.evaluate_state(board, self.ai_player), None

        valid_moves.sort(key=lambda m: Evaluator.score_move_quick(board, m[0], m[1], self.ai_player if is_maximizing else self.human_player), reverse=True)

        best_move = valid_moves[0]
        if is_maximizing:
            max_val = -float('inf')
            for r, c in valid_moves[:12]:
                board.make_move(r, c, self.ai_player)
                val, _ = self.minimax_search(board, depth - 1, False)
                board.undo_move(r, c, self.ai_player)
                if val > max_val:
                    max_val = val
                    best_move = (r, c)
            return max_val, best_move
        else:
            min_val = float('inf')
            for r, c in valid_moves[:12]:
                board.make_move(r, c, self.human_player)
                val, _ = self.minimax_search(board, depth - 1, True)
                board.undo_move(r, c, self.human_player)
                if val < min_val:
                    min_val = val
                    best_move = (r, c)
            return min_val, best_move

    def alpha_beta_search(self, board, depth, alpha, beta, is_maximizing):
        # Nâng cấp: Tối ưu Transposition Table với các cờ EXACT, LOWER, UPPER
        # EXACT = 0, LOWER = 1 (cắt tỉa Beta), UPPER = 2 (không vượt qua Alpha)
        state_key = (str(board.grid), is_maximizing)
        
        if state_key in self.memo:
            val, d, flag, m = self.memo[state_key]
            if d >= depth:
                if flag == 0: return val, m
                if flag == 1: alpha = max(alpha, val)
                if flag == 2: beta = min(beta, val)
                if alpha >= beta: return val, m

        self.states_evaluated += 1
        winner = board.check_winner(win_count=4)
        if winner is not None:
            if winner == self.ai_player: return 100000 + depth, None
            if winner == self.human_player: return -100000 - depth, None
            return 0, None
            
        if depth == 0:
            return Evaluator.evaluate_state(board, self.ai_player), None

        valid_moves = board.get_valid_moves(search_radius=2)
        if not valid_moves: return Evaluator.evaluate_state(board, self.ai_player), None

        valid_moves.sort(key=lambda m: Evaluator.score_move_quick(board, m[0], m[1], self.ai_player if is_maximizing else self.human_player), reverse=True)

        orig_alpha = alpha
        orig_beta = beta
        best_move = valid_moves[0]
        
        if is_maximizing:
            max_val = -float('inf')
            for r, c in valid_moves[:30]:
                board.make_move(r, c, self.ai_player)
                val, _ = self.alpha_beta_search(board, depth - 1, alpha, beta, False)
                board.undo_move(r, c, self.ai_player)
                
                if val > max_val:
                    max_val = val
                    best_move = (r, c)
                alpha = max(alpha, val)
                if beta <= alpha: break
                
            flag = 0
            if max_val <= orig_alpha: flag = 2 # UPPER
            elif max_val >= orig_beta: flag = 1 # LOWER
            self.memo[state_key] = (max_val, depth, flag, best_move)
            return max_val, best_move
            
        else:
            min_val = float('inf')
            for r, c in valid_moves[:30]:
                board.make_move(r, c, self.human_player)
                val, _ = self.alpha_beta_search(board, depth - 1, alpha, beta, True)
                board.undo_move(r, c, self.human_player)
                
                if val < min_val:
                    min_val = val
                    best_move = (r, c)
                beta = min(beta, val)
                if beta <= alpha: break
                
            flag = 0
            if min_val <= orig_alpha: flag = 2 # UPPER
            elif min_val >= orig_beta: flag = 1 # LOWER
            self.memo[state_key] = (min_val, depth, flag, best_move)
            return min_val, best_move
