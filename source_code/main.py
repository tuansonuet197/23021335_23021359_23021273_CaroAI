import pygame
import sys
sys.stdout.reconfigure(encoding='utf-8')
from board import Board
from ai import AI
from ui import GameUI

def main():
    ui = GameUI()
    ai = AI()
    
    # --- CẤU HÌNH THÔNG SỐ AI ---
    max_depth = 4 
    use_alpha_beta = True 
    WIN_COUNT = 4 
    # ----------------------------
    
    running = True
    board = Board(size=9)
    player_turn = True # Để bạn đi trước cho ổn định
    game_over = False
    
    status_msg = "Luot cua ban (X). Hay chon nuoc di!"
    status_color = (0, 0, 255)
    
    print("=== CHƯƠNG TRÌNH CHƠI CARO AI ===")
    print(f"Thuật toán: {'Alpha-Beta Pruning' if use_alpha_beta else 'Minimax gốc'}")
    print(f"Độ sâu tìm kiếm: {max_depth}")
    print(f"Luật: {WIN_COUNT} quân liên tiếp là thắng.")
    print("---------------------------------")
    
    ui.draw_board(board, status_msg, status_color)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # Xử lý khi người dùng click chuột
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    # CLICK ĐỂ CHƠI LẠI
                    board = Board(size=9)
                    game_over = False
                    player_turn = True
                    status_msg = "VAN MOI! Luot cua ban (X)."
                    status_color = (0, 0, 255)
                    ui.draw_board(board, status_msg, status_color)
                    print("\n--- VÁN MỚI ---")
                    continue
                
                if player_turn:
                    r, c = ui.get_click_pos(pygame.mouse.get_pos())
                    if r is not None and c is not None and board.make_move(r, c, 1): # 1 là Người
                        ui.draw_board(board, "May dang suy nghi...", (255, 0, 0))
                        # Vẽ ngay chữ "Máy đang suy nghĩ" để người chơi biết
                        pygame.display.update()
                        
                        winner = board.check_winner(win_count=WIN_COUNT)
                        if winner is not None:
                            game_over = True
                            if winner == 1: 
                                status_msg = "CHUC MUNG! BAN DA THANG! (Click de choi lai)"
                                status_color = (0, 150, 0)
                            else: 
                                status_msg = "HOA NHAU! (Click de choi lai)"
                                status_color = (0, 0, 0)
                            ui.draw_board(board, status_msg, status_color)
                        else:
                            player_turn = False
                        
        # Xử lý lượt của máy
        if not game_over and not player_turn:
            print("\nĐến lượt máy suy nghĩ...")
            move, score, states_evaluated, execution_time = ai.get_best_move(board, max_depth, use_alpha_beta)
            
            if move:
                r, c = move
                board.make_move(r, c, 2) # 2 là Máy
                
                # In ra các thông số theo yêu cầu của đề bài
                print(f"Máy đánh tại: ({r}, {c})")
                print(f"Giá trị đánh giá: {score}")
                print(f"Số trạng thái đã duyệt: {states_evaluated}")
                print(f"Thời gian chạy: {execution_time:.4f} giây")
                
                winner = board.check_winner(win_count=WIN_COUNT)
                if winner is not None:
                    game_over = True
                    if winner == 2: 
                        status_msg = "MAY DA THANG! (Click de choi lai)"
                        status_color = (255, 0, 0)
                    else: 
                        status_msg = "HOA NHAU! (Click de choi lai)"
                        status_color = (0, 0, 0)
                
                ui.draw_board(board, status_msg, status_color)
            
            # Đảm bảo luôn trả lại lượt cho người để tránh vòng lặp vô tận
            player_turn = True
                    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
