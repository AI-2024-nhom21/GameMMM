# menu.py

import pygame
from game.var import WIDTH, HEIGHT

# Trạng thái menu
MENU_MAIN = 0
MENU_MODE = 1
MENU_PLAY_TYPE = 2
MENU_HUMAN = 3
MENU_PAUSE = 4
GAME_RUNNING = 5

# Đường dẫn font và background
FONT_PATH = "assets/fonts/Asember Ligature Demo.ttf"
FONT_SIZE = 30
BACKGROUND_PATH = "assets/images/background/"

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Vị trí các nút trong từng menu
BUTTON_POSITIONS = {
    MENU_MAIN: [(345, 375), (345, 430)],  # Play Game, Quit
    MENU_MODE: [(345, 350), (345, 400), (345, 450)],  # Story, Random Map, Back
    MENU_PLAY_TYPE: [(345, 350), (345, 400), (345, 450)],  # Bot Play, Human Play, Back
    MENU_HUMAN: [(345, 350), (345, 400), (345, 450)],  # New Game, Load Game, Back
    MENU_PAUSE: [(100, 200), (100, 250), (100, 300), (100, 350), (100, 400)]  # Undo Step, Reset move, Options, World Map, Out to main
}

# Đường dẫn hình ảnh nút
BUTTON_IMAGES = {
    MENU_PAUSE: [
        "assets/images/buttons/undo.png",
        "assets/images/buttons/reset.png",
        "assets/images/buttons/options.png",
        "assets/images/buttons/world_map.png",
        "assets/images/buttons/out_main.png"
    ]
}

# Cấu hình các nút sidebar
BUTTON_SIDEBARS = [
    {
        "name": "Undo Move",
        "image": "assets/images/buttons/undo.png",
        "hover": "assets/images/buttons/undo_hover.png",
        "action": "undo_move"
    },
    {
        "name": "Reset Move",
        "image": "assets/images/buttons/reset.png",
        "hover": "assets/images/buttons/reset_hover.png",
        "action": "reset_move"
    },
    {
        "name": "World Map",
        "image": "assets/images/buttons/world_map.png",
        "hover": "assets/images/buttons/world_map_hover.png",
        "action": "world_map"
    },
    {
        "name": "Options",
        "image": "assets/images/buttons/options.png",
        "hover": "assets/images/buttons/options_hover.png",
        "action": "options"
    },
    {
        "name": "Out to Main",
        "image": "assets/images/buttons/out_main.png",
        "hover": "assets/images/buttons/out_main_hover.png",
        "action": "go_main_menu"
    }
]

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        self.menu_background = pygame.image.load(BACKGROUND_PATH + "menu.jpg")
        self.menu_background = pygame.transform.scale(self.menu_background, (WIDTH, HEIGHT))
        self.pause_background = pygame.image.load(BACKGROUND_PATH + "pause.jpg")
        self.pause_background = pygame.transform.scale(self.pause_background, (WIDTH, HEIGHT))
        self.current_menu = MENU_MAIN
        self.menu_stack = []
        self.selected_button = 0
        self.buttons = []
        self.play_type = None
        self.sidebar_buttons = []
        self.button_images = {}  # Cache cho hình ảnh nút
        self.load_button_images()

    def load_button_images(self):
        """Tải và lưu trữ hình ảnh nút để tối ưu hóa"""
        for button in BUTTON_SIDEBARS:
            img = pygame.image.load(button["image"])
            img = pygame.transform.scale(img, (100, 50))  # Kích thước nút sidebar
            hover_img = pygame.image.load(button["hover"])
            hover_img = pygame.transform.scale(hover_img, (100, 50))
            self.button_images[button["image"]] = img
            self.button_images[button["hover"]] = hover_img

    def draw_button(self, text, pos, index, color):
        """Vẽ nút với dấu >>> khi được chọn"""
        x, y = pos
        text_surf = self.font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        
        if index == self.selected_button:
            signal = self.font.render(">>>", True, color)
            signal_rect = signal.get_rect(midright=(text_rect.left - 10, text_rect.centery))
            self.screen.blit(signal, signal_rect)
        
        self.screen.blit(text_surf, text_rect)
        return text_rect

    def draw_sidebar(self, game_logic):
        """Vẽ sidebar với các nút khi game đang chạy"""
        self.sidebar_buttons = []
        mouse_pos = pygame.mouse.get_pos()
        
        for i, button in enumerate(BUTTON_SIDEBARS):
            x, y = 10, 50 + i * 60  # Vị trí nút trên sidebar
            img = self.button_images[button["hover"]] if self.is_mouse_over_button(x, y, mouse_pos) else self.button_images[button["image"]]
            button_rect = img.get_rect(topleft=(x, y))
            self.screen.blit(img, button_rect)
            self.sidebar_buttons.append((button_rect, button["action"]))

    def is_mouse_over_button(self, x, y, mouse_pos):
        """Kiểm tra xem chuột có đang ở trên nút không"""
        button_rect = pygame.Rect(x, y, 100, 50)
        return button_rect.collidepoint(mouse_pos)

    def draw_menu(self, game_logic=None):
        """Vẽ giao diện menu hoặc sidebar dựa trên trạng thái hiện tại"""
        self.buttons = []
        
        if self.current_menu == MENU_PAUSE:
            self.screen.blit(self.pause_background, (0, 0))
            button_images = BUTTON_IMAGES[self.current_menu]
            
            for i, img_path in enumerate(button_images):
                button_img = pygame.image.load(img_path)
                button_img = pygame.transform.scale(button_img, (200, 50))
                x, y = BUTTON_POSITIONS[self.current_menu][i]
                button_rect = button_img.get_rect(topleft=(x, y))
                self.screen.blit(button_img, button_rect)
                self.buttons.append(button_rect)
        elif self.current_menu == GAME_RUNNING and game_logic:
            # Vẽ game và sidebar
            game_logic.draw_map(game_logic.walls, game_logic.stair_pos, game_logic.stair_type, game_logic.player, game_logic.enemies)
            self.draw_sidebar(game_logic)
        else:
            self.screen.blit(self.menu_background, (0, 0))
            color = BLACK
            if self.current_menu == MENU_MAIN:
                texts = ["Play Game", "Quit"]
            elif self.current_menu == MENU_MODE:
                texts = ["Story", "Random Map", "Back"]
            elif self.current_menu == MENU_PLAY_TYPE:
                texts = ["Bot Play", "Human Play", "Back"]
            elif self.current_menu == MENU_HUMAN:
                texts = ["New Game", "Load Game", "Back"]

            for i, text in enumerate(texts):
                self.buttons.append(self.draw_button(text, BUTTON_POSITIONS[self.current_menu][i], i, color))
        
        pygame.display.flip()

    def handle_menu_input(self, event, game_logic=None):
        """Xử lý sự kiện phím và chuột trong menu hoặc sidebar"""
        if event.type == pygame.KEYDOWN and len(self.buttons) > 0:
            if event.key == pygame.K_DOWN:
                self.selected_button = (self.selected_button + 1) % len(self.buttons)
                self.draw_menu(game_logic)
            elif event.key == pygame.K_UP:
                self.selected_button = (self.selected_button - 1) % len(self.buttons)
                self.draw_menu(game_logic)
            elif event.key == pygame.K_RETURN:
                return self.handle_button_action(self.selected_button, game_logic)

        # Xử lý sự kiện chuột
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.current_menu == GAME_RUNNING:
                for button_rect, action in self.sidebar_buttons:
                    if button_rect.collidepoint(mouse_pos):
                        return self.handle_sidebar_action(action, game_logic)
            else:
                for i, button_rect in enumerate(self.buttons):
                    if button_rect.collidepoint(mouse_pos):
                        return self.handle_button_action(i, game_logic)

        return None

    def handle_button_action(self, selected_index, game_logic=None):
        """Thực hiện hành động tương ứng với nút được chọn"""
        if self.current_menu == MENU_MAIN:
            if selected_index == 0:  # Play Game
                self.menu_stack.append(self.current_menu)
                self.current_menu = MENU_MODE
                self.selected_button = 0
                self.draw_menu()
            elif selected_index == 1:  # Quit
                return False

        elif self.current_menu == MENU_MODE:
            if selected_index == 2:  # Back
                self.current_menu = self.menu_stack.pop()
                self.selected_button = 0
                self.draw_menu()
            else:
                self.menu_stack.append(self.current_menu)
                self.current_menu = MENU_PLAY_TYPE
                self.selected_button = 0
                self.draw_menu()

        elif self.current_menu == MENU_PLAY_TYPE:
            if selected_index == 2:  # Back
                self.current_menu = self.menu_stack.pop()
                self.selected_button = 0
                self.draw_menu()
            else:
                self.menu_stack.append(self.current_menu)
                self.current_menu = MENU_HUMAN
                self.selected_button = 0
                self.play_type = "BOT" if selected_index == 0 else "HUMAN"
                self.draw_menu()

        elif self.current_menu == MENU_HUMAN:
            if selected_index == 2:  # Back
                self.current_menu = self.menu_stack.pop()
                self.selected_button = 0
                self.draw_menu()
            else:
                self.current_menu = GAME_RUNNING
                return True

        elif self.current_menu == MENU_PAUSE:
            if selected_index == 0:  # Undo Move
                if game_logic:
                    game_logic.undo_move()
                    self.draw_menu(game_logic)
            elif selected_index == 1:  # Reset Move
                if game_logic:
                    game_logic.reset_move()
                    self.draw_menu(game_logic)
            elif selected_index == 2:  # Options
                print("Options menu opened")
            elif selected_index == 3:  # World Map
                print("World Map displayed")
            elif selected_index == 4:  # Out to Main
                self.current_menu = MENU_MAIN
                self.selected_button = 0
                self.draw_menu()
        
        return None

    def handle_sidebar_action(self, action, game_logic):
        """Xử lý hành động của nút sidebar"""
        if action == "undo_move" and game_logic:
            game_logic.undo_move()
            self.draw_menu(game_logic)
        elif action == "reset_move" and game_logic:
            game_logic.reset_move()
            self.draw_menu(game_logic)
        elif action == "world_map":
            print("World Map displayed")
            self.draw_menu(game_logic)
        elif action == "options":
            print("Options menu opened")
            self.draw_menu(game_logic)
        elif action == "go_main_menu":
            self.current_menu = MENU_MAIN
            self.selected_button = 0
            self.menu_stack = []
            self.draw_menu()
        return None