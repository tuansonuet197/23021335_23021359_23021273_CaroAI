import pygame

# Hằng số kích thước
WIDTH = 540
BOARD_HEIGHT = 540
INFO_HEIGHT = 60
HEIGHT = BOARD_HEIGHT + INFO_HEIGHT
CELL_SIZE = WIDTH // 9

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (220, 220, 220)
DARK_GREEN = (0, 150, 0)

class GameUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Caro AI - Minimax & Alpha-Beta")
        # Thay font hỗ trợ tiếng Việt cơ bản
        self.font = pygame.font.SysFont('segoeui', 22, bold=True)
        
    def draw_board(self, board, status_text="", text_color=BLACK):
        self.screen.fill(WHITE)
        
        # Vẽ lưới 9x9
        for i in range(10):
            pygame.draw.line(self.screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)
            pygame.draw.line(self.screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_HEIGHT), 2)
            
        # Vẽ các quân cờ
        for r in range(9):
            for c in range(9):
                if board.grid[r][c] == 1:
                    # Vẽ quân X (Người chơi - Màu Xanh)
                    pygame.draw.line(self.screen, BLUE, (c * CELL_SIZE + 10, r * CELL_SIZE + 10), ((c + 1) * CELL_SIZE - 10, (r + 1) * CELL_SIZE - 10), 3)
                    pygame.draw.line(self.screen, BLUE, ((c + 1) * CELL_SIZE - 10, r * CELL_SIZE + 10), (c * CELL_SIZE + 10, (r + 1) * CELL_SIZE - 10), 3)
                elif board.grid[r][c] == 2:
                    # Vẽ quân O (Máy - Màu Đỏ)
                    pygame.draw.circle(self.screen, RED, (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 10, 3)
                    
        # Vẽ thanh trạng thái bên dưới
        pygame.draw.rect(self.screen, GRAY, (0, BOARD_HEIGHT, WIDTH, INFO_HEIGHT))
        if status_text:
            text_surface = self.font.render(status_text, True, text_color)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, BOARD_HEIGHT + INFO_HEIGHT // 2))
            self.screen.blit(text_surface, text_rect)
            
        pygame.display.flip()

    def get_click_pos(self, pos):
        """
        Chuyển đổi tọa độ click chuột thành tọa độ dòng, cột trên bàn cờ.
        """
        x, y = pos
        if y >= BOARD_HEIGHT:
            return None, None
        return y // CELL_SIZE, x // CELL_SIZE
