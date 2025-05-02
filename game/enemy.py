# enemy.py

import pygame
from collections import deque
from game.var import ENEMY_RED_PATH, ENEMY_WHITE_PATH, CELL_SIZE

class Enemy:
    def __init__(self, enemy_pos, grid_size, walls, enemy_type="red"):
        self.enemy_pos = enemy_pos  # Vị trí [row, col]
        self.grid_size = grid_size
        self.walls = walls
        self.direction = "down"  # Hướng mặc định
        self.frame = 0  # Khung hình hiện tại
        self.animation_speed = 0.2
        self.animation_timer = 0
        self.enemy_type = enemy_type  # "red" hoặc "white"

        # Chọn đường dẫn hình ảnh dựa trên enemy_type
        enemy_path = ENEMY_RED_PATH if enemy_type == "red" else ENEMY_WHITE_PATH
        prefix = "er" if enemy_type == "red" else "ew"

        # Tải hình ảnh động
        self.animations = {
            "up": [
                pygame.transform.scale(pygame.image.load(enemy_path + f"up/{prefix}_up_0.png"), (CELL_SIZE, CELL_SIZE)),
                pygame.transform.scale(pygame.image.load(enemy_path + f"up/{prefix}_up_1.png"), (CELL_SIZE, CELL_SIZE))
            ],
            "down": [
                pygame.transform.scale(pygame.image.load(enemy_path + f"down/{prefix}_down_0.png"), (CELL_SIZE, CELL_SIZE)),
                pygame.transform.scale(pygame.image.load(enemy_path + f"down/{prefix}_down_1.png"), (CELL_SIZE, CELL_SIZE))
            ],
            "left": [
                pygame.transform.scale(pygame.image.load(enemy_path + f"left/{prefix}_left_0.png"), (CELL_SIZE, CELL_SIZE)),
                pygame.transform.scale(pygame.image.load(enemy_path + f"left/{prefix}_left_1.png"), (CELL_SIZE, CELL_SIZE))
            ],
            "right": [
                pygame.transform.scale(pygame.image.load(enemy_path + f"right/{prefix}_right_0.png"), (CELL_SIZE, CELL_SIZE)),
                pygame.transform.scale(pygame.image.load(enemy_path + f"right/{prefix}_right_1.png"), (CELL_SIZE, CELL_SIZE))
            ]
        }

    def is_wall_blocking(self, row1, col1, row2, col2):
        return (row1, col1, row2, col2) in self.walls or (row2, col2, row1, col1) in self.walls

    def bfs(self, target_pos):
        queue = deque([(self.enemy_pos, [self.enemy_pos])])
        visited = {tuple(self.enemy_pos)}

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Lên, xuống, trái, phải

        while queue:
            (row, col), path = queue.popleft()
            if [row, col] == target_pos:
                return path

            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                if (1 <= new_row <= self.grid_size and 1 <= new_col <= self.grid_size and
                        (new_row, new_col) not in visited and
                        not self.is_wall_blocking(row, col, new_row, new_col)):
                    visited.add((new_row, new_col))
                    queue.append(([new_row, new_col], path + [[new_row, new_col]]))

        return None

    def move_towards_player(self, player_pos):
        path = self.bfs(player_pos)
        if path and len(path) > 1:
            new_pos = path[1]
            # Cập nhật hướng dựa trên vị trí mới
            if new_pos[0] < self.enemy_pos[0]:
                self.direction = "up"
            elif new_pos[0] > self.enemy_pos[0]:
                self.direction = "down"
            elif new_pos[1] < self.enemy_pos[1]:
                self.direction = "left"
            elif new_pos[1] > self.enemy_pos[1]:
                self.direction = "right"
            self.enemy_pos = new_pos
        return self.enemy_pos

    def update_animation(self, delta_time):
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.frame = (self.frame + 1) % 2
            self.animation_timer = 0

    def draw(self, screen, start_x, start_y):
        x = start_x + (self.enemy_pos[1] - 1) * CELL_SIZE
        y = start_y + (self.enemy_pos[0] - 1) * CELL_SIZE
        screen.blit(self.animations[self.direction][self.frame], (x, y))