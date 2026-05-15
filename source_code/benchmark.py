import sys
sys.stdout.reconfigure(encoding='utf-8')
from board import Board
from ai import AI

def create_board_1():
    # 1. Trạng thái đầu ván (Bàn cờ trống)
    return Board(9)

def create_board_2():
    # 2. Trạng thái máy có thể thắng ngay (Đã có 3 quân ngang)
    b = Board(9)
    b.make_move(4, 4, 2)
    b.make_move(4, 5, 2)
    b.make_move(4, 6, 2)
    b.make_move(5, 4, 1)
    b.make_move(5, 5, 1)
    return b

def create_board_3():
    # 3. Trạng thái người chơi sắp thắng, máy cần chặn (Người có 3 quân chéo)
    b = Board(9)
    b.make_move(2, 2, 1)
    b.make_move(3, 3, 1)
    b.make_move(4, 4, 1)
    b.make_move(2, 5, 2)
    b.make_move(2, 6, 2)
    return b

def create_board_4():
    # 4. Trạng thái hai bên đều có cơ hội tấn công
    b = Board(9)
    b.make_move(4, 4, 1)
    b.make_move(4, 5, 2)
    b.make_move(5, 4, 2)
    b.make_move(5, 5, 1)
    b.make_move(3, 3, 1)
    b.make_move(6, 6, 2)
    return b

def create_board_5():
    # 5. Trạng thái có nhiều nước đi lân cận khiến thuật toán phải xét nhiều nhánh
    b = Board(9)
    moves = [(4,4,1), (4,5,2), (5,4,2), (5,5,1), (3,4,1), (6,4,2), (4,3,2), (4,6,1)]
    for r, c, p in moves:
        b.make_move(r, c, p)
    return b

def run_benchmark():
    ai = AI()
    boards = [
        ("Đầu ván", create_board_1()),
        ("Máy sắp thắng", create_board_2()),
        ("Người sắp thắng", create_board_3()),
        ("Cơ hội cân bằng", create_board_4()),
        ("Nhiều nước đi", create_board_5())
    ]
    
    depths = [1, 2, 3, 4] # Chạy thử ở 4 độ sâu khác nhau
    
    print("="*85)
    print(f"{'Tên Trạng Thái':<18} | {'Độ sâu':<6} | {'Thuật toán':<10} | {'Số TT xét':<10} | {'Thời gian (s)':<15}")
    print("="*85)
    
    for name, b in boards:
        for d in depths:
            # ---- Chạy Minimax ----
            # Lưu ý: Ở trạng thái đầu ván, depth=3 cho Minimax có thể mất vài chục giây
            # Nếu chạy quá lâu, bạn có thể comment lại và chỉ chạy alpha-beta
            _, _, states_mm, time_mm = ai.get_best_move(b.copy(), d, use_alpha_beta=False)
            print(f"{name:<18} | {d:<6} | {'Minimax':<10} | {states_mm:<10} | {time_mm:<15.4f}")
            
            # ---- Chạy Alpha-Beta ----
            _, _, states_ab, time_ab = ai.get_best_move(b.copy(), d, use_alpha_beta=True)
            print(f"{name:<18} | {d:<6} | {'Alpha-Beta':<10} | {states_ab:<10} | {time_ab:<15.4f}")
            print("-" * 85)

if __name__ == "__main__":
    run_benchmark()
