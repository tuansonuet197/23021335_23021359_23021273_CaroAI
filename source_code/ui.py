import pygame
import pygame.gfxdraw

class GameUI:
    def __init__(self, size=9, cell_size=55):
        pygame.init()
        self.size = size
        self.cell_size = cell_size
        self.margin = 80 # Thu hẹp margin
        
        self.grid_width = size * cell_size
        self.width = self.grid_width + self.margin * 2
        # Chiều cao cân đối hơn
        self.height = self.grid_width + self.margin * 2 + 80
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Caro AI Pro")
        
        # Colors
        self.BG_COLOR = (10, 10, 15)
        self.CARD_COLOR = (20, 20, 30)
        self.GRID_COLOR = (45, 45, 65)
        self.X_COLOR = (0, 255, 240)
        self.O_COLOR = (255, 45, 100)
        self.TEXT_COLOR = (230, 230, 240)
        self.SUB_TEXT = (130, 140, 160)
        self.ACCENT = (79, 70, 229)
        
        # Giảm kích thước Font chữ để tránh bị "to quá"
        try:
            self.title_font = pygame.font.SysFont("Segoe UI", 28, bold=True)
            self.font = pygame.font.SysFont("Segoe UI", 18, bold=True)
            self.small_font = pygame.font.SysFont("Segoe UI", 14)
        except:
            self.title_font = pygame.font.SysFont("Arial", 28, bold=True)
            self.font = pygame.font.SysFont("Arial", 18, bold=True)
            self.small_font = pygame.font.SysFont("Arial", 14)
        
        # Buttons (Thu nhỏ và sắp xếp lại)
        btn_y = self.height - 60
        btn_w, btn_h = 120, 35
        spacing = 15
        total_w = btn_w * 3 + spacing * 2
        start_x = (self.width - total_w) // 2
        
        self.restart_rect = pygame.Rect(start_x, btn_y, btn_w, btn_h)
        self.mode_rect = pygame.Rect(start_x + btn_w + spacing, btn_y, btn_w, btn_h)
        self.depth_rect = pygame.Rect(start_x + (btn_w + spacing) * 2, btn_y, btn_w, btn_h)

    def draw_board(self, board, status_msg, status_color, player_first, ai_mode, depth, stats=None):
        self.screen.fill(self.BG_COLOR)
        
        # Title
        title_surf = self.title_font.render("CARO AI PRO", True, self.TEXT_COLOR)
        self.screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 20))
        
        # Background bàn cờ
        pygame.draw.rect(self.screen, self.CARD_COLOR, (self.margin - 5, self.margin - 5, self.grid_width + 10, self.grid_width + 10), border_radius=10)
        
        # Lưới
        for i in range(self.size + 1):
            pos = self.margin + i * self.cell_size
            pygame.draw.line(self.screen, self.GRID_COLOR, (self.margin, pos), (self.margin + self.grid_width, pos), 1)
            pygame.draw.line(self.screen, self.GRID_COLOR, (pos, self.margin), (pos, self.margin + self.grid_width), 1)

        # Quân cờ (Vẽ nhỏ lại cho thanh thoát)
        for r in range(self.size):
            for c in range(self.size):
                piece = board.grid[r][c]
                cx = self.margin + c * self.cell_size + self.cell_size // 2
                cy = self.margin + r * self.cell_size + self.cell_size // 2
                if piece == 1: self.draw_x(cx, cy)
                elif piece == 2: self.draw_o(cx, cy)

        # Highlight nước cuối
        lm = board.last_move
        if lm:
            r, c = lm
            lx = self.margin + c * self.cell_size
            ly = self.margin + r * self.cell_size
            s = 8
            pygame.draw.lines(self.screen, (255, 255, 255), False, [(lx, ly+s), (lx, ly), (lx+s, ly)], 2)
            pygame.draw.lines(self.screen, (255, 255, 255), False, [(lx+self.cell_size-s, ly), (lx+self.cell_size, ly), (lx+self.cell_size, ly+s)], 2)
            pygame.draw.lines(self.screen, (255, 255, 255), False, [(lx+self.cell_size, ly+self.cell_size-s), (lx+self.cell_size, ly+self.cell_size), (lx+self.cell_size-s, ly+self.cell_size)], 2)
            pygame.draw.lines(self.screen, (255, 255, 255), False, [(lx+s, ly+self.cell_size), (lx, ly+self.cell_size), (lx, ly+self.cell_size-s)], 2)

        # Status
        status_surf = self.font.render(status_msg, True, status_color)
        self.screen.blit(status_surf, (self.width // 2 - status_surf.get_width() // 2, self.margin + self.grid_width + 15))

        # Stats
        if stats:
            stats_str = f"Nodes: {stats['states']:,}  |  Time: {stats['time']:.3f}s"
            stats_surf = self.small_font.render(stats_str, True, self.SUB_TEXT)
            self.screen.blit(stats_surf, (self.width // 2 - stats_surf.get_width() // 2, self.margin + self.grid_width + 45))

        # Buttons
        self.draw_button(self.restart_rect, "RESTART")
        self.draw_button(self.mode_rect, f"AI: {ai_mode}")
        self.draw_button(self.depth_rect, f"DEPTH: {depth}")

        pygame.display.flip()

    def draw_button(self, rect, text):
        mouse_pos = pygame.mouse.get_pos()
        color = (self.ACCENT[0]+20, self.ACCENT[1]+20, self.ACCENT[2]+20) if rect.collidepoint(mouse_pos) else self.ACCENT
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        text_surf = self.small_font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surf, (rect.x + (rect.width - text_surf.get_width()) // 2, rect.y + (rect.height - text_surf.get_height()) // 2))

    def draw_x(self, x, y):
        s = self.cell_size // 4
        pygame.draw.line(self.screen, self.X_COLOR, (x - s, y - s), (x + s, y + s), 3)
        pygame.draw.line(self.screen, self.X_COLOR, (x + s, y - s), (x - s, y + s), 3)

    def draw_o(self, x, y):
        r = self.cell_size // 4
        pygame.gfxdraw.aacircle(self.screen, x, y, r, self.O_COLOR)
        pygame.gfxdraw.filled_circle(self.screen, x, y, r, self.O_COLOR)
        pygame.gfxdraw.filled_circle(self.screen, x, y, r-3, self.CARD_COLOR)

    def get_click_pos(self, pos):
        x, y = pos
        if self.margin <= x < self.margin + self.grid_width and self.margin <= y < self.margin + self.grid_width:
            c = (x - self.margin) // self.cell_size
            r = (y - self.margin) // self.cell_size
            return r, c
        return None, None

    def check_button_click(self, pos):
        if self.restart_rect.collidepoint(pos): return "restart"
        if self.mode_rect.collidepoint(pos): return "mode"
        if self.depth_rect.collidepoint(pos): return "depth"
        return None
