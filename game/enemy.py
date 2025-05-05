# enemy.py

import pygame
from collections import deque
from game.var import ENEMY_RED_PATH, ENEMY_WHITE_PATH, CELL_SIZE

class Enemy:
    def __init__(self, enemy_pos, grid_size, walls, enemy_type="red"):
        self.enemy_pos = enemy_pos  # Vị trí [row, col]
        self.grid_size = grid_size
        self.walls = walls
        self.direction = "down"
        self.frame = 0
        self.animation_speed = 0.2
        self.animation_timer = 0
        self.enemy_type = enemy_type

        # 🔧 Tọa độ pixel để vẽ mượt
        self.x = (enemy_pos[1] - 1) * CELL_SIZE
        self.y = (enemy_pos[0] - 1) * CELL_SIZE
        self.target_x = self.x
        self.target_y = self.y
        self.moving = False
        self.move_speed = 150  # pixels per second 🔧

        enemy_path = ENEMY_RED_PATH if enemy_type == "red" else ENEMY_WHITE_PATH
        prefix = "er" if enemy_type == "red" else "ew"

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
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

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
            # Cập nhật hướng
            if new_pos[0] < self.enemy_pos[0]:
                self.direction = "up"
            elif new_pos[0] > self.enemy_pos[0]:
                self.direction = "down"
            elif new_pos[1] < self.enemy_pos[1]:
                self.direction = "left"
            elif new_pos[1] > self.enemy_pos[1]:
                self.direction = "right"

            self.enemy_pos = new_pos

            # 🔧 Cập nhật mục tiêu vẽ mượt
            self.target_x = (new_pos[1] - 1) * CELL_SIZE
            self.target_y = (new_pos[0] - 1) * CELL_SIZE
            self.moving = True
        return self.enemy_pos

    def update_animation(self, delta_time):
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.frame = (self.frame + 1) % 2
            self.animation_timer = 0

        # 🔧 Di chuyển mượt
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
        # 🔧 Vẽ theo x, y để hỗ trợ hoạt ảnh mượt
        screen.blit(self.animations[self.direction][self.frame],
                    (start_x + self.x, start_y + self.y))