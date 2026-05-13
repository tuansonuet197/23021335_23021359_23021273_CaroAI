import time
from evaluate import Evaluator

class AI:
    def __init__(self):
        self.states_evaluated = 0
        self.ai_player = 2
        self.human_player = 1

    def get_best_move(self, board, max_depth, use_alpha_beta=True, ai_player=2):
        self.states_evaluated = 0
        self.ai_player = ai_player
        self.human_player = 1 if ai_player == 2 else 2
        
        start_time = time.time()
        
        if use_alpha_beta:
            score, move = self.alpha_beta_search(board, max_depth, -float('inf'), float('inf'), True)
        else:
            score, move = self.minimax_search(board, max_depth, True)
            
        execution_time = time.time() - start_time
        return move, score, self.states_evaluated, execution_time

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
        if not valid_moves:
            return Evaluator.evaluate_state(board, self.ai_player), None

        # Sắp xếp nước đi để đưa những ô nguy hiểm lên đầu
        valid_moves.sort(key=lambda m: Evaluator.score_move_quick(board, m[0], m[1], self.ai_player if is_maximizing else self.human_player), reverse=True)

        best_move = valid_moves[0]
        if is_maximizing:
            max_val = -float('inf')
            for r, c in valid_moves[:12]: # Minimax thuần túy rất chậm nên giới hạn ít nước đi
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
        self.states_evaluated += 1
        winner = board.check_winner(win_count=4)
        if winner is not None:
            if winner == self.ai_player: return 100000 + depth, None
            if winner == self.human_player: return -100000 - depth, None
            return 0, None
        if depth == 0:
            return Evaluator.evaluate_state(board, self.ai_player), None

        valid_moves = board.get_valid_moves(search_radius=2)
        if not valid_moves:
            return Evaluator.evaluate_state(board, self.ai_player), None

        # Sắp xếp nước đi thông minh
        valid_moves.sort(key=lambda m: Evaluator.score_move_quick(board, m[0], m[1], self.ai_player if is_maximizing else self.human_player), reverse=True)

        best_move = valid_moves[0]
        if is_maximizing:
            max_val = -float('inf')
            for r, c in valid_moves[:25]: # Alpha-Beta có thể duyệt tới 25 nước đi
                board.make_move(r, c, self.ai_player)
                val, _ = self.alpha_beta_search(board, depth - 1, alpha, beta, False)
                board.undo_move(r, c, self.ai_player)
                if val > max_val:
                    max_val = val
                    best_move = (r, c)
                alpha = max(alpha, val)
                if beta <= alpha: break
            return max_val, best_move
        else:
            min_val = float('inf')
            for r, c in valid_moves[:25]:
                board.make_move(r, c, self.human_player)
                val, _ = self.alpha_beta_search(board, depth - 1, alpha, beta, True)
                board.undo_move(r, c, self.human_player)
                if val < min_val:
                    min_val = val
                    best_move = (r, c)
                beta = min(beta, val)
                if beta <= alpha: break
            return min_val, best_move
