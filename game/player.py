# player.py

import pygame
from game.var import EXPLORER_PATH, CELL_SIZE

class Player:
    def __init__(self, player_pos):
        self.player_pos = player_pos  # Vị trí [row, col]
        self.direction = "down"  # Hướng mặc định
        self.frame = 0  # Khung hình hiện tại (0 hoặc 1)
        self.animation_speed = 0.2  # Tốc độ chuyển đổi khung hình
        self.animation_timer = 0

        # Tải hình ảnh động
        self.animations = {
            "up": [
                pygame.transform.scale(pygame.image.load(EXPLORER_PATH + "up/ex_up_0.png"), (CELL_SIZE, CELL_SIZE)),
                pygame.transform.scale(pygame.image.load(EXPLORER_PATH + "up/ex_up_1.png"), (CELL_SIZE, CELL_SIZE))
            ],
            "down": [
                pygame.transform.scale(pygame.image.load(EXPLORER_PATH + "down/ex_down_0.png"), (CELL_SIZE, CELL_SIZE)),
                pygame.transform.scale(pygame.image.load(EXPLORER_PATH + "down/ex_down_1.png"), (CELL_SIZE, CELL_SIZE))
            ],
            "left": [
                pygame.transform.scale(pygame.image.load(EXPLORER_PATH + "left/ex_left_0.png"), (CELL_SIZE, CELL_SIZE)),
                pygame.transform.scale(pygame.image.load(EXPLORER_PATH + "left/ex_left_1.png"), (CELL_SIZE, CELL_SIZE))
            ],
            "right": [
                pygame.transform.scale(pygame.image.load(EXPLORER_PATH + "right/ex_right_0.png"), (CELL_SIZE, CELL_SIZE)),
                pygame.transform.scale(pygame.image.load(EXPLORER_PATH + "right/ex_right_1.png"), (CELL_SIZE, CELL_SIZE))
            ]
        }

    def move(self, new_pos, walls, grid_size):
        """Di chuyển player nếu không có tường chặn"""
        row1, col1 = self.player_pos
        row2, col2 = new_pos

        # Kiểm tra xem có tường chặn hay không
        if (1 <= new_pos[0] <= grid_size and 1 <= new_pos[1] <= grid_size and
                not ((row1, col1, row2, col2) in walls or (row2, col2, row1, col1) in walls)):
            # Cập nhật hướng dựa trên vị trí mới
            if new_pos[0] < self.player_pos[0]:
                self.direction = "up"
            elif new_pos[0] > self.player_pos[0]:
                self.direction = "down"
            elif new_pos[1] < self.player_pos[1]:
                self.direction = "left"
            elif new_pos[1] > self.player_pos[1]:
                self.direction = "right"
            self.player_pos = new_pos
            return True
        return False

    def update_animation(self, delta_time):
        """Cập nhật khung hình động"""
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.frame = (self.frame + 1) % 2  # Chuyển đổi giữa 0 và 1
            self.animation_timer = 0

    def draw(self, screen, start_x, start_y):
        """Vẽ player lên màn hình"""
        x = start_x + (self.player_pos[1] - 1) * CELL_SIZE
        y = start_y + (self.player_pos[0] - 1) * CELL_SIZE
        screen.blit(self.animations[self.direction][self.frame], (x, y))