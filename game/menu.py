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
        self.play_type = None  # Thêm dòng này
  

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
    def draw_menu(self):
        """Vẽ giao diện menu dựa trên trạng thái hiện tại"""
        self.buttons = []
        
        if self.current_menu == MENU_PAUSE:
            self.screen.blit(self.pause_background, (0, 0))
            button_images = BUTTON_IMAGES[self.current_menu]
            
            for i, img_path in enumerate(button_images):
                button_img = pygame.image.load(img_path)
                button_img = pygame.transform.scale(button_img, (200, 50))  # Tùy chỉnh kích thước
                x, y = BUTTON_POSITIONS[self.current_menu][i]
                button_rect = button_img.get_rect(topleft=(x, y))
                self.screen.blit(button_img, button_rect)
                self.buttons.append(button_rect)
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

    def handle_menu_input(self, event):
        """Xử lý sự kiện phím và chuột trong menu"""
        if event.type == pygame.KEYDOWN and len(self.buttons) > 0:
            if event.key == pygame.K_DOWN:
                self.selected_button = (self.selected_button + 1) % len(self.buttons)
                self.draw_menu()
            elif event.key == pygame.K_UP:
                self.selected_button = (self.selected_button - 1) % len(self.buttons)
                self.draw_menu()
            elif event.key == pygame.K_RETURN:
                return self.handle_button_action(self.selected_button)

        # Xử lý sự kiện chuột
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, button_rect in enumerate(self.buttons):
                if button_rect.collidepoint(mouse_pos):  
                    return self.handle_button_action(i)

        return None  # Tiếp tục ở menu hiện tại

    def handle_button_action(self, selected_index):
        """Thực hiện hành động tương ứng với nút được chọn"""
        if self.current_menu == MENU_MAIN:
            if selected_index == 0:  # Play Game
                self.menu_stack.append(self.current_menu)
                self.current_menu = MENU_MODE
                self.selected_button = 0
                self.draw_menu()
            elif selected_index == 1:  # Quit
                return False  # Thoát game

        elif self.current_menu == MENU_MODE:
            if selected_index == 2:  # Back
                self.current_menu = self.menu_stack.pop()
                self.selected_button = 0
                self.draw_menu()
            else:  # Story hoặc Random Map
                self.menu_stack.append(self.current_menu)
                self.current_menu = MENU_PLAY_TYPE
                self.selected_button = 0
                self.draw_menu()

        elif self.current_menu == MENU_PLAY_TYPE:
            if selected_index == 2:  # Back
                self.current_menu = self.menu_stack.pop()
                self.selected_button = 0
                self.draw_menu()
            else:  # Bot Play hoặc Human Play
                self.menu_stack.append(self.current_menu)
                self.current_menu = MENU_HUMAN
                self.selected_button = 0

                # Ghi nhớ loại người chơi
                if selected_index == 0:
                    self.play_type = "BOT"
                else:
                    self.play_type = "HUMAN"

                self.draw_menu()

        elif self.current_menu == MENU_HUMAN:
            if selected_index == 2:  # Back
                self.current_menu = self.menu_stack.pop()
                self.selected_button = 0
                self.draw_menu()
            else:  # New Game hoặc Load Game
                self.current_menu = GAME_RUNNING
                return True  # Chuyển sang chơi game

        elif self.current_menu == MENU_PAUSE:
            if selected_index == 0:  # Undo Move
                print("Undo Move executed")
            elif selected_index == 1:  # Reset Move
                print("Reset Move executed")
            elif selected_index == 2:  # Options
                print("Options menu opened")
            elif selected_index == 3:  # World Map
                print("World Map displayed")
            elif selected_index == 4:  # Out to Main
                self.current_menu = MENU_MAIN
                self.selected_button = 0
                self.draw_menu()
        
        return None  # Tiếp tục ở menu hiện tại
