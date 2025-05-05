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

        # 🔧 Thêm toạ độ pixel cho hoạt ảnh mượt
        self.x = (player_pos[1] - 1) * CELL_SIZE  # pixel x
        self.y = (player_pos[0] - 1) * CELL_SIZE  # pixel y
        self.target_x = self.x
        self.target_y = self.y
        self.moving = False
        self.move_speed = 150  # pixel per second 🔧

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

        if (1 <= new_pos[0] <= grid_size and 1 <= new_pos[1] <= grid_size and
                not ((row1, col1, row2, col2) in walls or (row2, col2, row1, col1) in walls)):
            # Cập nhật hướng
            if new_pos[0] < self.player_pos[0]:
                self.direction = "up"
            elif new_pos[0] > self.player_pos[0]:
                self.direction = "down"
            elif new_pos[1] < self.player_pos[1]:
                self.direction = "left"
            elif new_pos[1] > self.player_pos[1]:
                self.direction = "right"

            self.player_pos = new_pos

            # 🔧 Cập nhật vị trí mục tiêu để đi mượt
            self.target_x = (new_pos[1] - 1) * CELL_SIZE
            self.target_y = (new_pos[0] - 1) * CELL_SIZE
            self.moving = True

            return True
        return False

    def update_animation(self, delta_time):
        """🔧 Cập nhật khung hình động và di chuyển mượt"""
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.frame = (self.frame + 1) % 2
            self.animation_timer = 0

        if self.moving:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            step = self.move_speed * delta_time

            if distance < step or distance == 0:
                self.x = self.target_x
                self.y = self.target_y
                self.moving = False
            else:
                self.x += (step * dx / distance)
                self.y += (step * dy / distance)

    def draw(self, screen, start_x, start_y):
        """Vẽ player lên màn hình"""
        # 🔧 Vẽ theo x, y để hỗ trợ mượt
        screen.blit(self.animations[self.direction][self.frame],
                    (start_x + self.x, start_y + self.y))