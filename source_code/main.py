import pygame
import sys
sys.stdout.reconfigure(encoding='utf-8')
from board import Board
from ai import AI
from ui import GameUI

def main():
    ui = GameUI()
    ai = AI()

    board = Board(size=9)
    game_over = False
    player_turn = True 
    
    # --- CẤU HÌNH AI MẶC ĐỊNH ---
    # Nâng lên Depth 4 mặc định cho Alpha-Beta để máy thông minh hơn
    max_depth = 4
    use_alpha_beta = True 
    
    status_msg = "Your Turn (X). Mode: Alpha-Beta"
    status_color = ui.TEXT_COLOR
    stats = None

    running = True
    while running:
        ai_mode_str = "Alpha-Beta" if use_alpha_beta else "Minimax"
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                btn = ui.check_button_click(event.pos)
                
                if btn == "restart":
                    board = Board(size=9)
                    game_over = False
                    player_turn = True
                    status_msg = f"NEW GAME! Mode: {ai_mode_str}"
                    stats = None
                    continue
                
                if btn == "mode":
                    use_alpha_beta = not use_alpha_beta
                    ai_mode_str = "Alpha-Beta" if use_alpha_beta else "Minimax"
                    status_msg = f"Switched to {ai_mode_str}"
                    # Nếu là Minimax, hạ depth xuống 3 để tránh treo
                    if not use_alpha_beta: max_depth = 3
                    continue
                
                if btn == "depth":
                    # Cycle: 1 -> 2 -> 3 -> 4
                    max_depth = 1 if max_depth == 4 else max_depth + 1
                    status_msg = f"Depth set to {max_depth}"
                    continue

                if player_turn and not game_over:
                    r, c = ui.get_click_pos(event.pos)
                    if r is not None and c is not None and board.make_move(r, c, 1):
                        if board.check_winner() is not None:
                            game_over = True
                            status_msg = "VICTORY! YOU WON!"
                            status_color = (74, 222, 128)
                        else:
                            player_turn = False
                            status_msg = f"AI ({ai_mode_str}) is thinking..."

        if not game_over and not player_turn:
            move, score, states_count, t = ai.get_best_move(board, max_depth, use_alpha_beta, 2)
            
            if move:
                r, c = move
                board.make_move(r, c, 2)
                stats = {"states": states_count, "time": t, "score": score}
                
                print(f"Mode: {ai_mode_str} | Depth: {max_depth} | Move: ({r}, {c}) | States: {states_count} | Time: {t:.3f}s")
                
                winner = board.check_winner()
                if winner is not None:
                    game_over = True
                    if winner == 2:
                        status_msg = "AI DEFEATED YOU!"
                        status_color = ui.O_COLOR
                    else:
                        status_msg = "DRAW GAME!"
                else:
                    player_turn = True
                    status_msg = "Your Turn!"
            else:
                game_over = True
                status_msg = "DRAW GAME!"

        ui.draw_board(board, status_msg, status_color, True, ai_mode_str, max_depth, stats)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
