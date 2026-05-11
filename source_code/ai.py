import time
from evaluate import evaluate_state

class AI:
    def __init__(self):
        self.states_evaluated = 0

    def get_best_move(self, board, max_depth, use_alpha_beta=True):
        self.states_evaluated = 0
        start_time = time.time()
        
        score, move = self.alpha_beta(board, max_depth, -float('inf'), float('inf'), True)
        
        execution_time = time.time() - start_time
        return move, score, self.states_evaluated, execution_time

    def alpha_beta(self, board, depth, alpha, beta, is_maximizing):
        self.states_evaluated += 1
        winner = board.check_winner(win_count=4)
        if winner is not None or depth == 0:
            return evaluate_state(board), None

        valid_moves = board.get_valid_moves(search_radius=1)
        if not valid_moves:
            return evaluate_state(board), None

        # SẮP XẾP NƯỚC ĐI - Ưu tiên các nước gần trung tâm
        move_scores = []
        center = board.size // 2
        for r, c in valid_moves:
            score = (center - abs(r - center) - abs(c - center))
            move_scores.append(((r, c), score))
            
        move_scores.sort(key=lambda x: x[1], reverse=True)
        # Chỉ lấy top 8 nước đi để đảm bảo tốc độ
        top_moves = [m[0] for m in move_scores[:8]]

        best_move = top_moves[0] if top_moves else None

        if is_maximizing:
            best_score = -float('inf')
            for r, c in top_moves:
                board.make_move(r, c, 2)
                score, _ = self.alpha_beta(board, depth - 1, alpha, beta, False)
                board.undo_move(r, c, 2)
                
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
                alpha = max(alpha, score)
                if beta <= alpha: break
        else:
            best_score = float('inf')
            for r, c in top_moves:
                board.make_move(r, c, 1)
                score, _ = self.alpha_beta(board, depth - 1, alpha, beta, True)
                board.undo_move(r, c, 1)
                
                if score < best_score:
                    best_score = score
                    best_move = (r, c)
                beta = min(beta, score)
                if beta <= alpha: break

        return best_score, best_move
